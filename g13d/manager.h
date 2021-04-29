#ifndef MANAGER_H
#define MANAGER_H

#include <map>
#include <string>
#include <vector>

#include "action.h"
#include "device.h"

namespace G13 {

/*!
 * top level class, holds what would otherwise be in global variables
 */
class Manager {
 public:
  Manager();

  g13_keyindex find_g13_key_value(const std::string &keyname) const;
  std::string find_g13_key_name(g13_keyindex) const;

  linux_keyvalue find_input_key_value(const std::string &keyname) const;
  std::string find_input_key_name(linux_keyvalue) const;

  void set_logo(const std::string &fn) {
    logo_filename = fn;
  }
  int run();

  std::string string_config_value(const std::string &name) const;
  void set_string_config_value(const std::string &name, const std::string &val);

  std::string make_pipe_name(Device *d, bool is_input);

  void set_log_level(::boost::log::trivial::severity_level lvl);
  void set_log_level(const std::string &);

 protected:
  void init_keynames();
  void display_keys();
  void discover_g13s(libusb_device **devs, ssize_t count,
                     std::vector<Device *> &g13s);
  void cleanup();

  std::string logo_filename;
  libusb_device **devs;

  libusb_context *ctx;
  std::vector<Device *> g13s;

  std::map<g13_keyindex, std::string> g13_key_to_name;
  std::map<std::string, g13_keyindex> g13_name_to_key;
  std::map<linux_keyvalue, std::string> input_key_to_name;
  std::map<std::string, linux_keyvalue> input_name_to_key;

  std::map<std::string, std::string> _string_config_values;

  static bool running;
  static void set_stop(int);
};

// inlines

inline Manager &Action::manager() {
  return _keypad.manager();
}

inline const Manager &Action::manager() const {
  return _keypad.manager();
}

inline const Manager &Profile::manager() const {
  return _keypad.manager();
}

}  // namespace G13

#endif  // MANAGER_H
