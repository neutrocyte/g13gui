#include "action.h"

#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/foreach.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/preprocessor/seq/for_each.hpp>

#include "manager.h"
#include "repr.h"

namespace G13 {

Action::~Action() {
}

Action_Keys::Action_Keys(Device &keypad,
                                 const std::string &keys_string)
    : Action(keypad) {
  std::vector<std::string> keys;
  boost::split(keys, keys_string, boost::is_any_of("+"));

  BOOST_FOREACH (std::string const &key, keys) {
    auto kval = manager().find_input_key_value(key);
    if (kval == BAD_KEY_VALUE) {
      throw CommandException("create action unknown key : " + key);
    }
    _keys.push_back(kval);
  }

  std::vector<int> _keys;
}

Action_Keys::~Action_Keys() {
}

void Action_Keys::act(Device &g13, bool is_down) {
  for (auto key : _keys) {
    g13.send_event(EV_KEY, key, is_down);
    G13_LOG(trace, "sending KEY " << (is_down ? "DOWN " : "UP ") << key);
  }
}

void Action_Keys::dump(std::ostream &out) const {
  out << " SEND KEYS: ";

  for (size_t i = 0; i < _keys.size(); i++) {
    if (i) out << " + ";
    out << manager().find_input_key_name(_keys[i]);
  }
}

Action_PipeOut::Action_PipeOut(Device &keypad,
                                       const std::string &out)
    : Action(keypad),
      _out(out + "\n") {
}
Action_PipeOut::~Action_PipeOut() {
}

void Action_PipeOut::act(Device &kp, bool is_down) {
  if (is_down) {
    kp.write_output_pipe(_out);
  }
}

void Action_PipeOut::dump(std::ostream &o) const {
  o << "WRITE PIPE : " << repr(_out);
}

Action_Command::Action_Command(Device &keypad,
                                       const std::string &cmd)
    : Action(keypad),
      _cmd(cmd) {
}
Action_Command::~Action_Command() {
}

void Action_Command::act(Device &kp, bool is_down) {
  if (is_down) {
    keypad().command(_cmd.c_str());
  }
}

void Action_Command::dump(std::ostream &o) const {
  o << "COMMAND : " << repr(_cmd);
}

}  // namespace G13
