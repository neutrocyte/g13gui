#ifndef STICK_H
#define STICK_H

#include "coord.h"
#include "bounds.h"
#include "action.h"

namespace G13 {

class G13_Stick;

typedef Coord<int> G13_StickCoord;
typedef Bounds<int> G13_StickBounds;
typedef Coord<double> G13_ZoneCoord;
typedef Bounds<double> G13_ZoneBounds;

class G13_StickZone : public G13_Actionable<G13_Stick> {
public:
  G13_StickZone(G13_Stick &, const std::string &name, const G13_ZoneBounds &,
                G13_ActionPtr = 0);

  bool operator==(const G13_StickZone &other) const {
    return _name == other._name;
  }

  void dump(std::ostream &) const;

  void parse_key(unsigned char *byte, G13_Device *g13);
  void test(const G13_ZoneCoord &loc);
  void set_bounds(const G13_ZoneBounds &bounds) { _bounds = bounds; }

protected:
  bool _active;
  G13_ZoneBounds _bounds;
};

typedef boost::shared_ptr<G13_StickZone> G13_StickZonePtr;

class G13_Stick {
public:
  G13_Stick(G13_Device &keypad);

  void parse_joystick(unsigned char *buf);

  void set_mode(stick_mode_t);
  G13_StickZone *zone(const std::string &, bool create = false);
  void remove_zone(const G13_StickZone &zone);

  const std::vector<G13_StickZone> &zones() const { return _zones; }

  void dump(std::ostream &) const;

protected:
  void _recalc_calibrated();

  G13_Device &_keypad;
  std::vector<G13_StickZone> _zones;

  G13_StickBounds _bounds;
  G13_StickCoord _center_pos;
  G13_StickCoord _north_pos;

  G13_StickCoord _current_pos;

  stick_mode_t _stick_mode;
};

} // namespace G13

#endif // STICK_H
