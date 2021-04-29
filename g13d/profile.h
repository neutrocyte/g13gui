#ifndef PROFILE_H
#define PROFILE_H

#include <memory>
#include <ostream>

#include "action.h"

/*! G13_KEY_SEQ is a Boost Preprocessor sequence containing the
 * G13 keys.  The order is very specific, with the position of each
 * item corresponding to a specific bit in the G13's USB message
 * format.  Do NOT remove or insert items in this list.
 */
#define G13_KEY_SEQ                                                         \
  /* byte 3 */ (G1)(G2)(G3)(G4)(G5)(G6)(G7)(G8) /* byte 4 */                \
      (G9)(G10)(G11)(G12)(G13)(G14)(G15)(G16) /* byte 5 */ (G17)(G18)(G19)( \
          G20)(G21)(G22)(UNDEF1)(LIGHT_STATE) /* byte 6 */                  \
      (BD)(L1)(L2)(L3)(L4)(M1)(M2)(M3) /* byte 7 */ (MR)(LEFT)(DOWN)(TOP)(  \
          UNDEF3)(LIGHT)(LIGHT2)(MISC_TOGGLE)

/*! G13_NONPARSED_KEY_SEQ is a Boost Preprocessor sequence containing the
 * G13 keys that shouldn't be tested input.  These aren't actually keys,
 * but they are in the bitmap defined by G13_KEY_SEQ.
 */
#define G13_NONPARSED_KEY_SEQ \
  (UNDEF1)(LIGHT_STATE)(UNDEF3)(LIGHT)(LIGHT2)(UNDEF3)(MISC_TOGGLE)

/*! KB_INPUT_KEY_SEQ is a Boost Preprocessor sequence containing the
 * names of keyboard keys we can send through binding actions.
 * These correspond to KEY_xxx value definitions in <linux/input.h>,
 * i.e. ESC is KEY_ESC, 1 is KEY_1, etc.
 */
#define KB_INPUT_KEY_SEQ                                                       \
  (ESC)(1)(2)(3)(4)(5)(6)(7)(8)(9)(0)(MINUS)(EQUAL)(BACKSPACE)(TAB)(Q)(W)(E)(  \
      R)(T)(Y)(U)(I)(O)(P)(LEFTBRACE)(RIGHTBRACE)(ENTER)(LEFTCTRL)(RIGHTCTRL)( \
      A)(S)(D)(F)(G)(H)(J)(K)(L)(SEMICOLON)(APOSTROPHE)(GRAVE)(LEFTSHIFT)(     \
      BACKSLASH)(Z)(X)(C)(V)(B)(N)(M)(COMMA)(DOT)(SLASH)(RIGHTSHIFT)(          \
      KPASTERISK)(LEFTALT)(RIGHTALT)(SPACE)(CAPSLOCK)(F1)(F2)(F3)(F4)(F5)(F6)( \
      F7)(F8)(F9)(F10)(F11)(F12)(NUMLOCK)(SCROLLLOCK)(KP7)(KP8)(KP9)(KPMINUS)( \
      KP4)(KP5)(KP6)(KPPLUS)(KP1)(KP2)(KP3)(KP0)(KPDOT)(LEFT)(RIGHT)(UP)(      \
      DOWN)(PAGEUP)(PAGEDOWN)(HOME)(END)(INSERT)(DELETE)

namespace G13 {

class Device;
class Key;
class Profile;

/*! manages the bindings for a G13 key
 *
 */
class Key : public Actionable<Profile> {
 public:
  void dump(std::ostream &o) const;
  g13_keyindex index() const {
    return _index.index;
  }

  void parse_key(unsigned char *byte, Device *g13);

 protected:
  struct KeyIndex {
    KeyIndex(int key) : index(key), offset(key / 8), mask(1 << (key % 8)) {
    }

    int index;
    unsigned char offset;
    unsigned char mask;
  };

  // Profile is the only class able to instantiate Keys
  friend class Profile;

  Key(Profile &mode, const std::string &name, int index)
      : Actionable<Profile>(mode, name),
        _index(index),
        _should_parse(true) {
  }

  Key(Profile &mode, const Key &key)
      : Actionable<Profile>(mode, key.name()),
        _index(key._index),
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
class Profile {
 public:
  Profile(Device &keypad, const std::string &name_arg)
      : _keypad(keypad),
        _name(name_arg) {
    _init_keys();
  }

  Profile(const Profile &other, const std::string &name_arg)
      : _keypad(other._keypad),
        _name(name_arg),
        _keys(other._keys) {
  }

  // search key by G13 keyname
  Key *find_key(const std::string &keyname);

  void dump(std::ostream &o) const;

  void parse_keys(unsigned char *buf);
  const std::string &name() const {
    return _name;
  }

  const Manager &manager() const;

 protected:
  Device &_keypad;
  std::string _name;
  std::vector<Key> _keys;

  void _init_keys();
};

typedef std::shared_ptr<Profile> ProfilePtr;

}  // namespace G13

#endif  // PROFILE_H
