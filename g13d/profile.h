#ifndef PROFILE_H
#define PROFILE_H

#include <memory>
#include <ostream>

#include "action.h"

namespace G13 {

class G13_Device;
class G13_Key;
class G13_Profile;

/*! manages the bindings for a G13 key
 *
 */
class G13_Key : public G13_Actionable<G13_Profile> {
public:
  void dump(std::ostream &o) const;
  G13_KEY_INDEX index() const { return _index.index; }

  void parse_key(unsigned char *byte, G13_Device *g13);

protected:
  struct KeyIndex {
    KeyIndex(int key) : index(key), offset(key / 8), mask(1 << (key % 8)) {}

    int index;
    unsigned char offset;
    unsigned char mask;
  };

  // G13_Profile is the only class able to instantiate G13_Keys
  friend class G13_Profile;

  G13_Key(G13_Profile &mode, const std::string &name, int index)
      : G13_Actionable<G13_Profile>(mode, name), _index(index),
        _should_parse(true) {
  }

  G13_Key(G13_Profile &mode, const G13_Key &key)
      : G13_Actionable<G13_Profile>(mode, key.name()), _index(key._index),
        _should_parse(key._should_parse) {
    set_action(key.action());
  }

  KeyIndex _index;
  bool _should_parse;
};

/*!
 * Represents a set of configured key mappings
 *
 * This allows a keypad to have multiple configured
 * profiles and switch between them easily
 */
class G13_Profile {
public:
  G13_Profile(G13_Device &keypad, const std::string &name_arg)
      : _keypad(keypad), _name(name_arg) {
    _init_keys();
  }

  G13_Profile(const G13_Profile &other, const std::string &name_arg)
      : _keypad(other._keypad), _name(name_arg), _keys(other._keys) {
  }

  // search key by G13 keyname
  G13_Key *find_key(const std::string &keyname);

  void dump(std::ostream &o) const;

  void parse_keys(unsigned char *buf);
  const std::string &name() const { return _name; }

  const G13_Manager &manager() const;

protected:
  G13_Device &_keypad;
  std::string _name;
  std::vector<G13_Key> _keys;

  void _init_keys();
};

typedef std::shared_ptr<G13_Profile> ProfilePtr;

} // namespace G13

#endif // PROFILE_H
