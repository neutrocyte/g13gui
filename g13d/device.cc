#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <signal.h>

#include <libusb-1.0/libusb.h>
#include <linux/uinput.h>

#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include <boost/foreach.hpp>

#include <iostream>
#include <fstream>
#include <string>

#include "logo.h"
#include "manager.h"
#include "repr.h"
#include "device.h"

namespace G13 {

static std::string describe_libusb_error_code(int code) {

#define TEST_libusb_error(r, data, elem)                                       \
  case BOOST_PP_CAT(LIBUSB_, elem):                                            \
    return BOOST_PP_STRINGIZE(elem);

  switch (code) {
    BOOST_PP_SEQ_FOR_EACH(
        TEST_libusb_error, _,
        (SUCCESS)(ERROR_IO)(ERROR_INVALID_PARAM)(ERROR_ACCESS)(ERROR_NO_DEVICE)(
            ERROR_NOT_FOUND)(ERROR_BUSY)(ERROR_TIMEOUT)(ERROR_OVERFLOW)(
            ERROR_PIPE)(ERROR_INTERRUPTED)(ERROR_NO_MEM)(ERROR_NOT_SUPPORTED)(
            ERROR_OTHER))
  }
  return "unknown error";
}

int g13_create_fifo(const char *fifo_name) {
  mkfifo(fifo_name, 0666);
  chmod(fifo_name, 0660);
  return open(fifo_name, O_RDWR | O_NONBLOCK);
}

int g13_create_uinput(void) {
  struct uinput_user_dev uinp;
  const char *dev_uinput_fname =
      access("/dev/input/uinput", F_OK) == 0
          ? "/dev/input/uinput"
          : access("/dev/uinput", F_OK) == 0 ? "/dev/uinput" : 0;
  if (!dev_uinput_fname) {
    G13_LOG(error, "Could not find an uinput device");
    return -1;
  }
  if (access(dev_uinput_fname, W_OK) != 0) {
    G13_LOG(error, dev_uinput_fname << " doesn't grant write permissions");
    return -1;
  }
  int ufile = open(dev_uinput_fname, O_WRONLY | O_NDELAY);
  if (ufile <= 0) {
    G13_LOG(error, "Could not open uinput");
    return -1;
  }
  memset(&uinp, 0, sizeof(uinp));
  char name[] = "G13";
  strncpy(uinp.name, name, sizeof(uinp.name));
  uinp.id.version = 1;
  uinp.id.bustype = BUS_USB;
  uinp.id.product = G13_PRODUCT_ID;
  uinp.id.vendor = G13_VENDOR_ID;
  uinp.absmin[ABS_X] = 0;
  uinp.absmin[ABS_Y] = 0;
  uinp.absmax[ABS_X] = 0xff;
  uinp.absmax[ABS_Y] = 0xff;
  //  uinp.absfuzz[ABS_X] = 4;
  //  uinp.absfuzz[ABS_Y] = 4;
  //  uinp.absflat[ABS_X] = 0x80;
  //  uinp.absflat[ABS_Y] = 0x80;

  ioctl(ufile, UI_SET_EVBIT, EV_KEY);
  ioctl(ufile, UI_SET_EVBIT, EV_ABS);
  /*  ioctl(ufile, UI_SET_EVBIT, EV_REL);*/
  ioctl(ufile, UI_SET_MSCBIT, MSC_SCAN);
  ioctl(ufile, UI_SET_ABSBIT, ABS_X);
  ioctl(ufile, UI_SET_ABSBIT, ABS_Y);
  /*  ioctl(ufile, UI_SET_RELBIT, REL_X);
   ioctl(ufile, UI_SET_RELBIT, REL_Y);*/
  for (int i = 0; i < 256; i++)
    ioctl(ufile, UI_SET_KEYBIT, i);
  ioctl(ufile, UI_SET_KEYBIT, BTN_THUMB);

  int retcode = write(ufile, &uinp, sizeof(uinp));
  if (retcode < 0) {
    G13_LOG(error, "Could not write to uinput device (" << retcode << ")");
    return -1;
  }
  retcode = ioctl(ufile, UI_DEV_CREATE);
  if (retcode) {
    G13_LOG(error, "Error creating uinput device for G13");
    return -1;
  }
  return ufile;
}

void G13_Device::send_event(int type, int code, int val) {
  memset(&_event, 0, sizeof(_event));
  gettimeofday(&_event.time, 0);
  _event.type = type;
  _event.code = code;
  _event.value = val;

  // TODO(jtgans): Make this actually verify it writes all bytes
  auto result = write(_uinput_fid, &_event, sizeof(_event));
  if (result < 0) {
    G13_LOG(error, "Unable to send event: " << strerror(errno));
    exit(1);
  }
}

void G13_Device::write_output_pipe(const std::string &out) {
  // TODO(jtgans): Make this actually verify it writes all bytes
  auto result = write(_output_pipe_fid, out.c_str(), out.size());
  if (result < 0) {
    G13_LOG(error, "Unable to write to output pipe: " << strerror(errno));
    exit(1);
  }
}

void G13_Device::set_mode_leds(int leds) {
  unsigned char usb_data[] = {5, 0, 0, 0, 0};
  usb_data[1] = leds;
  int r = libusb_control_transfer(
      handle, LIBUSB_REQUEST_TYPE_CLASS | LIBUSB_RECIPIENT_INTERFACE, 9, 0x305,
      0, usb_data, 5, 1000);

  if (r != 5) {
    G13_LOG(error, "Problem sending data");
    return;
  }
}

void G13_Device::set_key_color(int red, int green, int blue) {
  int error;
  unsigned char usb_data[] = {5, 0, 0, 0, 0};
  usb_data[1] = red;
  usb_data[2] = green;
  usb_data[3] = blue;

  error = libusb_control_transfer(
      handle, LIBUSB_REQUEST_TYPE_CLASS | LIBUSB_RECIPIENT_INTERFACE, 9, 0x307,
      0, usb_data, 5, 1000);
  if (error != 5) {
    G13_LOG(error, "Problem sending data");
    return;
  }
}

void G13_Device::register_context(libusb_context *_ctx) {
  ctx = _ctx;

  int leds = 0;
  int red = 0;
  int green = 0;
  int blue = 255;
  init_lcd();

  set_mode_leds(leds);
  set_key_color(red, green, blue);

  write_lcd(g13_logo, sizeof(g13_logo));

  _uinput_fid = g13_create_uinput();

  _input_pipe_name = _manager.make_pipe_name(this, true);
  _input_pipe_fid = g13_create_fifo(_input_pipe_name.c_str());
  _output_pipe_name = _manager.make_pipe_name(this, false);
  _output_pipe_fid = g13_create_fifo(_output_pipe_name.c_str());

  if (_input_pipe_fid == -1) {
    G13_LOG(error, "failed opening pipe");
  }
}

void G13_Device::cleanup() {
  remove(_input_pipe_name.c_str());
  remove(_output_pipe_name.c_str());
  ioctl(_uinput_fid, UI_DEV_DESTROY);
  close(_uinput_fid);
  libusb_release_interface(handle, 0);
  libusb_close(handle);
}


/*! reads and processes key state report from G13
 *
 */
int G13_Device::read_keys() {
  unsigned char buffer[G13_REPORT_SIZE];
  int size;
  int error =
      libusb_interrupt_transfer(handle, LIBUSB_ENDPOINT_IN | G13_KEY_ENDPOINT,
                                buffer, G13_REPORT_SIZE, &size, 100);

  if (error && error != LIBUSB_ERROR_TIMEOUT) {

    G13_LOG(error, "Error while reading keys: "
                       << error << " (" << describe_libusb_error_code(error)
                       << ")");
    //    G13_LOG( error, "Stopping daemon" );
    //    return -1;
  }
  if (size == G13_REPORT_SIZE) {
    parse_joystick(buffer);
    _current_profile->parse_keys(buffer);
    send_event(EV_SYN, SYN_REPORT, 0);
  }
  return 0;
}

void G13_Device::read_config_file(const std::string &filename) {
  std::ifstream s(filename);

  G13_LOG(info, "reading configuration from " << filename);
  while (s.good()) {

    // grab a line
    char buf[1024];
    buf[0] = 0;
    buf[sizeof(buf) - 1] = 0;
    s.getline(buf, sizeof(buf) - 1);

    // strip comment
    char *comment = strchr(buf, '#');
    if (comment) {
      comment--;
      while (comment > buf && isspace(*comment))
        comment--;
      *comment = 0;
    }

    // send it
    if (buf[0]) {
      G13_LOG(info, "  cfg: " << buf);
      command(buf);
    }
  }
}

void G13_Device::read_commands() {

  fd_set set;
  FD_ZERO(&set);
  FD_SET(_input_pipe_fid, &set);
  struct timeval tv;
  tv.tv_sec = 0;
  tv.tv_usec = 0;
  int ret = select(_input_pipe_fid + 1, &set, 0, 0, &tv);
  if (ret > 0) {
    unsigned char buf[1024 * 1024];
    memset(buf, 0, 1024 * 1024);
    ret = read(_input_pipe_fid, buf, 1024 * 1024);
    G13_LOG(trace, "read " << ret << " characters");

    if (ret ==
        960) { // TODO probably image, for now, don't test, just assume image
      lcd().image(buf, ret);
    } else {
      std::string buffer = reinterpret_cast<const char *>(buf);
      std::vector<std::string> lines;
      boost::split(lines, buffer, boost::is_any_of("\n\r"));

      BOOST_FOREACH (std::string const &cmd, lines) {
        std::vector<std::string> command_comment;
        boost::split(command_comment, cmd, boost::is_any_of("#"));

        if (command_comment.size() > 0 &&
            command_comment[0] != std::string("")) {
          G13_LOG(info, "command: " << command_comment[0]);
          command(command_comment[0].c_str());
        }
      }
    }
  }
}

G13_Device::G13_Device(G13_Manager &manager, libusb_device_handle *handle,
                       int _id)
    : _id_within_manager(_id), handle(handle), ctx(0), _uinput_fid(-1),
      _manager(manager), _lcd(*this), _stick(*this) {
  _current_profile = ProfilePtr(new G13_Profile(*this, "default"));
  _profiles["default"] = _current_profile;

  for (unsigned int i = 0; i < sizeof(keys); i++) {
    keys[i] = false;
  }

  lcd().image_clear();

  _init_fonts();
  _init_commands();
}

FontPtr G13_Device::switch_to_font(const std::string &name) {
  FontPtr rv = _fonts[name];
  if (rv) {
    _current_font = rv;
  }
  return rv;
}

void G13_Device::switch_to_profile(const std::string &name) {
  _current_profile = profile(name);
}

ProfilePtr G13_Device::profile(const std::string &name) {
  ProfilePtr rv = _profiles[name];
  if (!rv) {
    rv = ProfilePtr(new G13_Profile(*_current_profile, name));
    _profiles[name] = rv;
  }
  return rv;
}


G13_ActionPtr G13_Device::make_action(const std::string &action) {
  if (!action.size()) {
    throw G13_CommandException("empty action string");
  }
  if (action[0] == '>') {
    return G13_ActionPtr(new G13_Action_PipeOut(*this, &action[1]));
  } else if (action[0] == '!') {
    return G13_ActionPtr(new G13_Action_Command(*this, &action[1]));
  } else {
    return G13_ActionPtr(new G13_Action_Keys(*this, action));
  }
  throw G13_CommandException("can't create action for " + action);
}

// *************************************************************************

void G13_Device::dump(std::ostream &o, int detail) {
  o << "G13 id=" << id_within_manager() << std::endl
    << "   input_pipe_name=" << repr(_input_pipe_name) << std::endl
    << "   output_pipe_name=" << repr(_output_pipe_name) << std::endl
    << "   current_profile=" << _current_profile->name() << std::endl
    << "   current_font=" << _current_font->name() << std::endl;

  if (detail > 0) {
    o << "STICK" << std::endl;

    stick().dump(o);

    if (detail == 1) {
      _current_profile->dump(o);
    } else {
      for (auto i = _profiles.begin(); i != _profiles.end(); i++) {
        i->second->dump(o);
      }
    }
  }
}

inline const char *advance_ws(const char* &source, std::string &dest) {
  const char *space = source ? strchr(source, ' ') : 0;

  if (space) {
    dest = std::string(source, space - source);
    source = space + 1;
  } else {
    dest = source;
    source = 0;
  }

  return source;
};

struct command_adder {
  command_adder(G13_Device::CommandFunctionTable &t, const char *name)
      : _t(t), _name(name) {}

  G13_Device::CommandFunctionTable &_t;
  std::string _name;
  command_adder &operator+=(G13_Device::COMMAND_FUNCTION f) {
    _t[_name] = f;
    return *this;
  };
};

#define RETURN_FAIL(message)                                                   \
  {                                                                            \
    G13_LOG(error, message);                                                   \
    return;                                                                    \
  }

#define G13_DEVICE_COMMAND(name)                                               \
  ;                                                                            \
  command_adder BOOST_PP_CAT(add_, name)(_command_table,                       \
                                         BOOST_PP_STRINGIZE(name));            \
  BOOST_PP_CAT(add_, name) += [this](const char *remainder)

void G13_Device::_init_commands() {
  G13_DEVICE_COMMAND(out) {
    lcd().write_string(remainder);
  }

  G13_DEVICE_COMMAND(pos) {
    int row, col;
    if (sscanf(remainder, "%i %i", &row, &col) == 2) {
      lcd().write_pos(row, col);
    } else {
      RETURN_FAIL("bad pos : " << remainder);
    }
  }

  G13_DEVICE_COMMAND(bind) {
    std::string keyname;
    advance_ws(remainder, keyname);
    std::string action = remainder;
    try {
      if (auto key = _current_profile->find_key(keyname)) {
        key->set_action(make_action(action));
      } else if (auto stick_key = _stick.zone(keyname)) {
        stick_key->set_action(make_action(action));
      } else {
        RETURN_FAIL("bind key " << keyname << " unknown");
      }
      G13_LOG(trace, "bind " << keyname << " [" << action << "]");
    } catch (const std::exception &ex) {
      RETURN_FAIL("bind " << keyname << " " << action
                          << " failed : " << ex.what());
    }
  }

  G13_DEVICE_COMMAND(profile) { switch_to_profile(remainder); }
  G13_DEVICE_COMMAND(font) { switch_to_font(remainder); }
  G13_DEVICE_COMMAND(mod) { set_mode_leds(atoi(remainder)); }
  G13_DEVICE_COMMAND(textmode) { lcd().text_mode = atoi(remainder); }

  G13_DEVICE_COMMAND(rgb) {
    int red, green, blue;
    if (sscanf(remainder, "%i %i %i", &red, &green, &blue) == 3) {
      set_key_color(red, green, blue);
    } else {
      RETURN_FAIL("rgb bad format: <" << remainder << ">");
    }
  }

#define STICKMODE_TEST(r, data, elem)                                          \
  if (mode == BOOST_PP_STRINGIZE(elem)) {                                      \
    _stick.set_mode(BOOST_PP_CAT(STICK_, elem));                               \
    return;                                                                    \
  } else

  G13_DEVICE_COMMAND(stickmode) {
    std::string mode = remainder;

    BOOST_PP_SEQ_FOR_EACH(
        STICKMODE_TEST, _,
        (ABSOLUTE)(RELATIVE)(KEYS)(CALCENTER)(CALBOUNDS)(CALNORTH)) {
      RETURN_FAIL("unknown stick mode : <" << mode << ">");
    }
  }

  G13_DEVICE_COMMAND(stickzone) {
    std::string operation, zonename;
    advance_ws(remainder, operation);
    advance_ws(remainder, zonename);

    if (operation != "add") {
      G13_StickZone *zone = _stick.zone(zonename);

      if (!zone) {
        throw G13_CommandException("unknown stick zone");
      }

      if (operation == "action") {
        zone->set_action(make_action(remainder));
      } else if (operation == "bounds") {
        double x1, y1, x2, y2;

        if (sscanf(remainder, "%lf %lf %lf %lf", &x1, &y1, &x2, &y2) != 4) {
          throw G13_CommandException("bad bounds format");
        }

        zone->set_bounds(G13_ZoneBounds(x1, y1, x2, y2));
      } else if (operation == "del") {
        _stick.remove_zone(*zone);
      } else {
        RETURN_FAIL("unknown stickzone operation: <" << operation << ">");
      }
    }
  }

  G13_DEVICE_COMMAND(dump) {
    std::string target;
    advance_ws(remainder, target);
    if (target == "all") {
      dump(std::cout, 3);
    } else if (target == "current") {
      dump(std::cout, 1);
    } else if (target == "summary") {
      dump(std::cout, 0);
    } else {
      RETURN_FAIL("unknown dump target: <" << target << ">");
    }
  }

  G13_DEVICE_COMMAND(log_level) {
    std::string level;
    advance_ws(remainder, level);
    manager().set_log_level(level);
  }

  G13_DEVICE_COMMAND(refresh) {
    lcd().image_send();
  }

  G13_DEVICE_COMMAND(clear) {
    lcd().image_clear();
    lcd().image_send();
  };
}

void G13_Device::command(char const *str) {
  const char *remainder = str;

  try {
    std::string cmd;
    advance_ws(remainder, cmd);

    auto i = _command_table.find(cmd);
    if (i == _command_table.end()) {
      RETURN_FAIL("unknown command : " << cmd)
    }

    COMMAND_FUNCTION f = i->second;
    f(remainder);

    return;
  } catch (const std::exception &ex) {
    RETURN_FAIL("command failed : " << ex.what());
  }
}


void G13_Device::init_lcd() {
  int error = libusb_control_transfer(handle, 0, 9, 1, 0, 0, 0, 1000);
  if (error) {
    G13_LOG(error, "Error when initializing lcd endpoint");
  }
}

void G13_Device::write_lcd(unsigned char *data, size_t size) {
  init_lcd();
  if (size != G13_LCD_BUFFER_SIZE) {
    G13_LOG(error, "Invalid LCD data size " << size << ", should be "
                                            << G13_LCD_BUFFER_SIZE);
    return;
  }
  unsigned char buffer[G13_LCD_BUFFER_SIZE + 32];
  memset(buffer, 0, G13_LCD_BUFFER_SIZE + 32);
  buffer[0] = 0x03;
  memcpy(buffer + 32, data, G13_LCD_BUFFER_SIZE);
  int bytes_written;
  int error = libusb_interrupt_transfer(
      handle, LIBUSB_ENDPOINT_OUT | G13_LCD_ENDPOINT, buffer,
      G13_LCD_BUFFER_SIZE + 32, &bytes_written, 1000);
  if (error)
    G13_LOG(error, "Error when transferring image: "
                       << error << ", " << bytes_written << " bytes written");
}

void G13_Device::write_lcd_file(const std::string &filename) {
  std::filebuf *pbuf;
  std::ifstream filestr;
  size_t size;

  filestr.open(filename.c_str());
  pbuf = filestr.rdbuf();

  size = pbuf->pubseekoff(0, std::ios::end, std::ios::in);
  pbuf->pubseekpos(0, std::ios::in);

  char buffer[size];

  pbuf->sgetn(buffer, size);

  filestr.close();
  write_lcd((unsigned char *)buffer, size);
}

void G13_Device::parse_joystick(unsigned char *buf) {
  _stick.parse_joystick(buf);
}

} // namespace G13
