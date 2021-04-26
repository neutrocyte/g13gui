#include "action.h"

#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/foreach.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/preprocessor/seq/for_each.hpp>

#include "manager.h"
#include "repr.h"

namespace G13 {

G13_Action::~G13_Action() {
}

G13_Action_Keys::G13_Action_Keys(G13_Device &keypad,
                                 const std::string &keys_string)
    : G13_Action(keypad) {
  std::vector<std::string> keys;
  boost::split(keys, keys_string, boost::is_any_of("+"));

  BOOST_FOREACH (std::string const &key, keys) {
    auto kval = manager().find_input_key_value(key);
    if (kval == BAD_KEY_VALUE) {
      throw G13_CommandException("create action unknown key : " + key);
    }
    _keys.push_back(kval);
  }

  std::vector<int> _keys;
}

G13_Action_Keys::~G13_Action_Keys() {
}

void G13_Action_Keys::act(G13_Device &g13, bool is_down) {
  for (auto key : _keys) {
    g13.send_event(EV_KEY, key, is_down);
    G13_LOG(trace, "sending KEY " << (is_down ? "DOWN " : "UP ") << key);
  }
}

void G13_Action_Keys::dump(std::ostream &out) const {
  out << " SEND KEYS: ";

  for (size_t i = 0; i < _keys.size(); i++) {
    if (i) out << " + ";
    out << manager().find_input_key_name(_keys[i]);
  }
}

G13_Action_PipeOut::G13_Action_PipeOut(G13_Device &keypad,
                                       const std::string &out)
    : G13_Action(keypad),
      _out(out + "\n") {
}
G13_Action_PipeOut::~G13_Action_PipeOut() {
}

void G13_Action_PipeOut::act(G13_Device &kp, bool is_down) {
  if (is_down) {
    kp.write_output_pipe(_out);
  }
}

void G13_Action_PipeOut::dump(std::ostream &o) const {
  o << "WRITE PIPE : " << repr(_out);
}

G13_Action_Command::G13_Action_Command(G13_Device &keypad,
                                       const std::string &cmd)
    : G13_Action(keypad),
      _cmd(cmd) {
}
G13_Action_Command::~G13_Action_Command() {
}

void G13_Action_Command::act(G13_Device &kp, bool is_down) {
  if (is_down) {
    keypad().command(_cmd.c_str());
  }
}

void G13_Action_Command::dump(std::ostream &o) const {
  o << "COMMAND : " << repr(_cmd);
}

}  // namespace G13
