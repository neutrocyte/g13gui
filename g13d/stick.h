#ifndef STICK_H
#define STICK_H

#include "action.h"
#include "bounds.h"
#include "coord.h"

namespace G13 {

class Stick;

typedef Coord<int> StickCoord;
typedef Bounds<int> StickBounds;
typedef Coord<double> ZoneCoord;
typedef Bounds<double> ZoneBounds;

class StickZone : public Actionable<Stick> {
 public:
  StickZone(Stick &, const std::string &name, const ZoneBounds &,
                ActionPtr = 0);

  bool operator==(const StickZone &other) const {
    return _name == other._name;
  }

  void dump(std::ostream &) const;

  void parse_key(unsigned char *byte, Device *g13);
  void test(const ZoneCoord &loc);
  void set_bounds(const ZoneBounds &bounds) {
    _bounds = bounds;
  }

 protected:
  bool _active;
  ZoneBounds _bounds;
};

typedef boost::shared_ptr<StickZone> StickZonePtr;

class Stick {
 public:
  Stick(Device &keypad);

  void parse_joystick(unsigned char *buf);

  void set_mode(stick_mode_t);
  StickZone *zone(const std::string &, bool create = false);
  void remove_zone(const StickZone &zone);

  const std::vector<StickZone> &zones() const {
    return _zones;
  }

  void dump(std::ostream &) const;

 protected:
  void _recalc_calibrated();

  Device &_keypad;
  std::vector<StickZone> _zones;

  StickBounds _bounds;
  StickCoord _center_pos;
  StickCoord _north_pos;

  StickCoord _current_pos;

  stick_mode_t _stick_mode;
};

}  // namespace G13

#endif  // STICK_H
