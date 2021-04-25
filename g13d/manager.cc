#include <signal.h>

#include <boost/log/attributes.hpp>
#include <boost/log/core/core.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/expressions/formatters/stream.hpp>
#include <boost/log/sources/severity_feature.hpp>
#include <boost/log/sources/severity_logger.hpp>
#include <boost/log/support/date_time.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/utility/setup.hpp>
#include <boost/log/utility/setup/console.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include <boost/preprocessor/stringize.hpp>
#include <boost/foreach.hpp>

#include <fstream>
#include <vector>

#include "helper.h"
#include "device.h"
#include "manager.h"
#include "find_or_throw.h"
#include "repr.h"

namespace G13 {

void G13_Manager::discover_g13s(libusb_device **devs, ssize_t count,
                                std::vector<G13_Device *> &g13s) {
  for (int i = 0; i < count; i++) {
    libusb_device_descriptor desc;
    int r = libusb_get_device_descriptor(devs[i], &desc);
    if (r < 0) {
      G13_LOG(error, "Failed to get device descriptor");
      return;
    }
    if (desc.idVendor == G13_VENDOR_ID && desc.idProduct == G13_PRODUCT_ID) {
      libusb_device_handle *handle;
      int r = libusb_open(devs[i], &handle);
      if (r != 0) {
        G13_LOG(error, "Error opening G13 device");
        return;
      }
      if (libusb_kernel_driver_active(handle, 0) == 1)
        if (libusb_detach_kernel_driver(handle, 0) == 0)
          G13_LOG(info, "Kernel driver detached");

      r = libusb_claim_interface(handle, 0);
      if (r < 0) {
        G13_LOG(error, "Cannot Claim Interface");
        return;
      }
      g13s.push_back(new G13_Device(*this, handle, g13s.size()));
    }
  }
}

void G13_Manager::set_log_level(::boost::log::trivial::severity_level lvl) {
  boost::log::core::get()->set_filter(::boost::log::trivial::severity >= lvl);
  G13_OUT("set log level to " << lvl);
}

void G13_Manager::set_log_level(const std::string &level) {

#define CHECK_LEVEL(L)                                                         \
  if (level == BOOST_PP_STRINGIZE(L)) {                                        \
    set_log_level(::boost::log::trivial::L);                                   \
    return;                                                                    \
  }

  CHECK_LEVEL(trace);
  CHECK_LEVEL(debug);
  CHECK_LEVEL(info);
  CHECK_LEVEL(warning);
  CHECK_LEVEL(error);
  CHECK_LEVEL(fatal);

  G13_LOG(error, "unknown log level" << level);
}

void G13_Manager::cleanup() {
  G13_LOG(info, "cleaning up");

  for (auto device : g13s) {
    device->cleanup();
    delete device;
  }

  libusb_exit(ctx);
}


G13_Manager::G13_Manager()
    : devs(0), ctx(0) {
}

// *************************************************************************

bool G13_Manager::running = true;
void G13_Manager::set_stop(int) { running = false; }

std::string G13_Manager::string_config_value(const std::string &name) const {
  try {
    return find_or_throw(_string_config_values, name);
  } catch (...) {
    return "";
  }
}

void G13_Manager::set_string_config_value(const std::string &name,
                                          const std::string &value) {
  G13_LOG(info, "set_string_config_value " << name << " = " << repr(value));
  _string_config_values[name] = value;
}

#define CONTROL_DIR std::string("/tmp/")

std::string G13_Manager::make_pipe_name(G13_Device *d, bool is_input) {
  if (is_input) {
    std::string config_base = string_config_value("pipe_in");
    if (config_base.size()) {
      if (d->id_within_manager() == 0) {
        return config_base;
      } else {
        return config_base + "-" +
               boost::lexical_cast<std::string>(d->id_within_manager());
      }
    }
    return CONTROL_DIR + "g13-" +
           boost::lexical_cast<std::string>(d->id_within_manager());
  } else {
    std::string config_base = string_config_value("pipe_out");
    if (config_base.size()) {
      if (d->id_within_manager() == 0) {
        return config_base;
      } else {
        return config_base + "-" +
               boost::lexical_cast<std::string>(d->id_within_manager());
      }
    }

    return CONTROL_DIR + "g13-" +
           boost::lexical_cast<std::string>(d->id_within_manager()) + "_out";
  }
}

int G13_Manager::run() {
  init_keynames();
  display_keys();

  ssize_t cnt;
  int ret;

  ret = libusb_init(&ctx);
  if (ret < 0) {
    G13_LOG(error, "Initialization error: " << ret);
    return 1;
  }

  libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, 3);
  cnt = libusb_get_device_list(ctx, &devs);
  if (cnt < 0) {
    G13_LOG(error, "Error while getting device list");
    return 1;
  }

  discover_g13s(devs, cnt, g13s);
  libusb_free_device_list(devs, 1);
  G13_LOG(info, "Found " << g13s.size() << " G13s");
  if (g13s.size() == 0) {
    return 1;
  }

  for (auto device : g13s) {
    device->register_context(ctx);
  }

  signal(SIGINT, set_stop);

  if (g13s.size() > 0 && logo_filename.size()) {
    g13s[0]->write_lcd_file(logo_filename);
  }

  G13_LOG(info, "Active Stick zones ");
  g13s[0]->stick().dump(std::cout);

  std::string config_fn = string_config_value("config");
  if (config_fn.size()) {
    G13_LOG(info, "config_fn = " << config_fn);
    g13s[0]->read_config_file(config_fn);
  }

  do {
    if (g13s.size() > 0)
      for (auto device : g13s) {
        int status = device->read_keys();
        device->read_commands();

        if (status < 0) {
          running = false;
        }
      }
  } while (running && (g13s.size() > 0));

  cleanup();

  return 0;
}

// setup maps to let us convert between strings and G13 key names
#define ADD_G13_KEY_MAPPING(r, data, elem)                                     \
  {                                                                            \
    std::string name = BOOST_PP_STRINGIZE(elem);                               \
    g13_key_to_name[key_index] = name;                                         \
    g13_name_to_key[name] = key_index;                                         \
    key_index++;                                                               \
  }

// setup maps to let us convert between strings and linux key names
#define ADD_KB_KEY_MAPPING(r, data, elem)                                      \
  {                                                                            \
    std::string name = BOOST_PP_STRINGIZE(elem);                               \
    int keyval = BOOST_PP_CAT(KEY_, elem);                                     \
    input_key_to_name[keyval] = name;                                          \
    input_name_to_key[name] = keyval;                                          \
  }

void G13_Manager::init_keynames() {
  int key_index = 0;

  BOOST_PP_SEQ_FOR_EACH(ADD_G13_KEY_MAPPING, _, G13_KEY_SEQ);
  BOOST_PP_SEQ_FOR_EACH(ADD_KB_KEY_MAPPING, _, KB_INPUT_KEY_SEQ);
}

LINUX_KEY_VALUE
G13_Manager::find_g13_key_value(const std::string &keyname) const {
  auto i = g13_name_to_key.find(keyname);
  if (i == g13_name_to_key.end()) {
    return BAD_KEY_VALUE;
  }
  return i->second;
}

LINUX_KEY_VALUE
G13_Manager::find_input_key_value(const std::string &keyname) const {

  // if there is a KEY_ prefix, strip it off
  if (!strncmp(keyname.c_str(), "KEY_", 4)) {
    return find_input_key_value(keyname.c_str() + 4);
  }

  auto i = input_name_to_key.find(keyname);
  if (i == input_name_to_key.end()) {
    return BAD_KEY_VALUE;
  }
  return i->second;
}

std::string G13_Manager::find_input_key_name(LINUX_KEY_VALUE v) const {
  try {
    return find_or_throw(input_key_to_name, v);
  } catch (...) {
    return "(unknown linux key)";
  }
}

std::string G13_Manager::find_g13_key_name(G13_KEY_INDEX v) const {
  try {
    return find_or_throw(g13_key_to_name, v);
  } catch (...) {
    return "(unknown G13 key)";
  }
}

void G13_Manager::display_keys() {
  G13_OUT("Known keys on G13:");
  G13_OUT(Helper::map_keys_out(g13_name_to_key));

  G13_OUT("Known keys to map to:");
  G13_OUT(Helper::map_keys_out(input_name_to_key));
}

} // namespace G13
