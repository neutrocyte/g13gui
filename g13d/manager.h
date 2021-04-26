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
class G13_Manager {
 public:
  G13_Manager();

  G13_KEY_INDEX find_g13_key_value(const std::string &keyname) const;
  std::string find_g13_key_name(G13_KEY_INDEX) const;

  LINUX_KEY_VALUE find_input_key_value(const std::string &keyname) const;
  std::string find_input_key_name(LINUX_KEY_VALUE) const;

  void set_logo(const std::string &fn) {
    logo_filename = fn;
  }
  int run();

  std::string string_config_value(const std::string &name) const;
  void set_string_config_value(const std::string &name, const std::string &val);

  std::string make_pipe_name(G13_Device *d, bool is_input);

  void set_log_level(::boost::log::trivial::severity_level lvl);
  void set_log_level(const std::string &);

 protected:
  void init_keynames();
  void display_keys();
  void discover_g13s(libusb_device **devs, ssize_t count,
                     std::vector<G13_Device *> &g13s);
  void cleanup();

  std::string logo_filename;
  libusb_device **devs;

  libusb_context *ctx;
  std::vector<G13_Device *> g13s;

  std::map<G13_KEY_INDEX, std::string> g13_key_to_name;
  std::map<std::string, G13_KEY_INDEX> g13_name_to_key;
  std::map<LINUX_KEY_VALUE, std::string> input_key_to_name;
  std::map<std::string, LINUX_KEY_VALUE> input_name_to_key;

  std::map<std::string, std::string> _string_config_values;

  static bool running;
  static void set_stop(int);
};

// *************************************************************************

// inlines

inline G13_Manager &G13_Action::manager() {
  return _keypad.manager();
}

inline const G13_Manager &G13_Action::manager() const {
  return _keypad.manager();
}

inline const G13_Manager &G13_Profile::manager() const {
  return _keypad.manager();
}

}  // namespace G13

#endif  // MANAGER_H
