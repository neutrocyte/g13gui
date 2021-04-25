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

#include <fstream>
#include <vector>

#include "device.h"
#include "manager.h"

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
} // namespace G13
