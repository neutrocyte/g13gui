#ifndef ACTION_H
#define ACTION_H

#include <memory>
#include <ostream>
#include <vector>

#include "g13.h"

namespace G13 {

class G13_Device;
class G13_Manager;

/*! holds potential actions which can be bound to G13 activity
 *
 */
class G13_Action {
 public:
  G13_Action(G13_Device &keypad) : _keypad(keypad) {
  }

  virtual ~G13_Action();

  virtual void act(G13_Device &, bool is_down) = 0;
  virtual void dump(std::ostream &) const = 0;

  void act(bool is_down) {
    act(keypad(), is_down);
  }

  G13_Device &keypad() {
    return _keypad;
  }
  const G13_Device &keypad() const {
    return _keypad;
  }

  G13_Manager &manager();
  const G13_Manager &manager() const;

 private:
  G13_Device &_keypad;
};

/*!
 * action to send one or more keystrokes
 */
class G13_Action_Keys : public G13_Action {
 public:
  G13_Action_Keys(G13_Device &keypad, const std::string &keys);
  virtual ~G13_Action_Keys();

  virtual void act(G13_Device &, bool is_down);
  virtual void dump(std::ostream &) const;

  std::vector<LINUX_KEY_VALUE> _keys;
};

/*!
 * action to send a string to the output pipe
 */
class G13_Action_PipeOut : public G13_Action {
 public:
  G13_Action_PipeOut(G13_Device &keypad, const std::string &out);
  virtual ~G13_Action_PipeOut();

  virtual void act(G13_Device &, bool is_down);
  virtual void dump(std::ostream &) const;

  std::string _out;
};

/*!
 * action to send a command to the g13
 */
class G13_Action_Command : public G13_Action {
 public:
  G13_Action_Command(G13_Device &keypad, const std::string &cmd);
  virtual ~G13_Action_Command();

  virtual void act(G13_Device &, bool is_down);
  virtual void dump(std::ostream &) const;

  std::string _cmd;
};

typedef std::shared_ptr<G13_Action> G13_ActionPtr;

template <class PARENT_T>
class G13_Actionable {
 public:
  G13_Actionable(PARENT_T &parent_arg, const std::string &name)
      : _name(name),
        _parent_ptr(&parent_arg) {
  }

  virtual ~G13_Actionable() {
    _parent_ptr = 0;
  }

  G13_ActionPtr action() const {
    return _action;
  }
  const std::string &name() const {
    return _name;
  }
  PARENT_T &parent() {
    return *_parent_ptr;
  }
  const PARENT_T &parent() const {
    return *_parent_ptr;
  }
  G13_Manager &manager() {
    return _parent_ptr->manager();
  }
  const G13_Manager &manager() const {
    return _parent_ptr->manager();
  }

  virtual void set_action(const G13_ActionPtr &action) {
    _action = action;
  }

 protected:
  std::string _name;
  G13_ActionPtr _action;

 private:
  PARENT_T *_parent_ptr;
};

}  // namespace G13

#endif  // ACTION_H
