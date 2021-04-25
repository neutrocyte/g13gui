

#include "device.h"

namespace G13 {

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

} // namespace G13
