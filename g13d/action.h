#ifndef ACTION_H
#define ACTION_H

#include <memory>
#include <ostream>
#include <vector>

#include "g13.h"

namespace G13 {

class Device;
class Manager;

/*! holds potential actions which can be bound to G13 activity
 *
 */
class Action {
 public:
  Action(Device &keypad) : _keypad(keypad) {
  }

  virtual ~Action();

  virtual void act(Device &, bool is_down) = 0;
  virtual void dump(std::ostream &) const = 0;

  void act(bool is_down) {
    act(keypad(), is_down);
  }

  Device &keypad() {
    return _keypad;
  }
  const Device &keypad() const {
    return _keypad;
  }

  Manager &manager();
  const Manager &manager() const;

 private:
  Device &_keypad;
};

/*!
 * action to send one or more keystrokes
 */
class Action_Keys : public Action {
 public:
  Action_Keys(Device &keypad, const std::string &keys);
  virtual ~Action_Keys();

  virtual void act(Device &, bool is_down);
  virtual void dump(std::ostream &) const;

  std::vector<LINUX_KEY_VALUE> _keys;
};

/*!
 * action to send a string to the output pipe
 */
class Action_PipeOut : public Action {
 public:
  Action_PipeOut(Device &keypad, const std::string &out);
  virtual ~Action_PipeOut();

  virtual void act(Device &, bool is_down);
  virtual void dump(std::ostream &) const;

  std::string _out;
};

/*!
 * action to send a command to the g13
 */
class Action_Command : public Action {
 public:
  Action_Command(Device &keypad, const std::string &cmd);
  virtual ~Action_Command();

  virtual void act(Device &, bool is_down);
  virtual void dump(std::ostream &) const;

  std::string _cmd;
};

typedef std::shared_ptr<Action> ActionPtr;

template <class PARENT_T>
class Actionable {
 public:
  Actionable(PARENT_T &parent_arg, const std::string &name)
      : _name(name),
        _parent_ptr(&parent_arg) {
  }

  virtual ~Actionable() {
    _parent_ptr = 0;
  }

  ActionPtr action() const {
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
  Manager &manager() {
    return _parent_ptr->manager();
  }
  const Manager &manager() const {
    return _parent_ptr->manager();
  }

  virtual void set_action(const ActionPtr &action) {
    _action = action;
  }

 protected:
  std::string _name;
  ActionPtr _action;

 private:
  PARENT_T *_parent_ptr;
};

}  // namespace G13

#endif  // ACTION_H
