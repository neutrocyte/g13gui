/* This file contains code for managing keys an profiles
 *
 */

#include "profile.h"

#include <boost/foreach.hpp>
#include <boost/preprocessor/seq/for_each.hpp>

#include "find_or_throw.h"
#include "helper.h"
#include "manager.h"
#include "repr.h"

namespace G13 {
// *************************************************************************

void Key::dump(std::ostream &o) const {
  o << manager().find_g13_key_name(index()) << "(" << index() << ") : ";

  if (action()) {
    action()->dump(o);
  } else {
    o << "(no action)";
  }
}

void Key::parse_key(unsigned char *byte, Device *g13) {
  bool key_is_down = byte[_index.offset] & _index.mask;
  bool key_state_changed = g13->update(_index.index, key_is_down);

  if (key_state_changed && _action) {
    _action->act(*g13, key_is_down);
  }
}

void Profile::_init_keys() {
  int key_index = 0;

  // create a Key entry for every key in G13_KEY_SEQ
#define INIT_KEY(r, data, elem)                                \
  {                                                            \
    Key key(*this, BOOST_PP_STRINGIZE(elem), key_index++); \
    _keys.push_back(key);                                      \
  }

  BOOST_PP_SEQ_FOR_EACH(INIT_KEY, _, G13_KEY_SEQ)

  assert(_keys.size() == G13_NUM_KEYS);

  // now disable testing for keys in G13_NONPARSED_KEY_SEQ
#define MARK_NON_PARSED_KEY(r, data, elem)             \
  {                                                    \
    Key *key = find_key(BOOST_PP_STRINGIZE(elem)); \
    assert(key);                                       \
    key->_should_parse = false;                        \
  }

  BOOST_PP_SEQ_FOR_EACH(MARK_NON_PARSED_KEY, _, G13_NONPARSED_KEY_SEQ)
}

void Profile::dump(std::ostream &o) const {
  o << "Profile " << repr(name()) << std::endl;
  BOOST_FOREACH (const Key &key, _keys) {
    if (key.action()) {
      o << "   ";
      key.dump(o);
      o << std::endl;
    }
  }
}
void Profile::parse_keys(unsigned char *buf) {
  buf += 3;
  for (size_t i = 0; i < _keys.size(); i++) {
    if (_keys[i]._should_parse) {
      _keys[i].parse_key(buf, &_keypad);
    }
  }
}

Key *Profile::find_key(const std::string &keyname) {
  auto key = _keypad.manager().find_g13_key_value(keyname);

  // TODO(jtgans): Check this is the proper type
  if (key >= 0 && key < static_cast<int>(_keys.size())) {
    return &_keys[key];
  }

  return 0;
}

}  // namespace G13
