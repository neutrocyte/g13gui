#ifndef BOUNDS_H
#define BOUNDS_H

#include <ostream>

#include "coord.h"

namespace G13 {

template <class T>
class Bounds {
 public:
  Bounds(const Coord<T> &_tl, const Coord<T> &_br) : tl(_tl), br(_br) {
  }

  Bounds(T x1, T y1, T x2, T y2) : tl(x1, y1), br(x2, y2) {
  }

  bool contains(const Coord<T> &pos) const {
    return tl.x <= pos.x && tl.y <= pos.y && pos.x <= br.x && pos.y <= br.y;
  }

  void expand(const Coord<T> &pos) {
    if (pos.x < tl.x) tl.x = pos.x;
    if (pos.y < tl.y) tl.y = pos.y;
    if (pos.x > br.x) br.x = pos.x;
    if (pos.y > br.y) br.y = pos.y;
  }

  Coord<T> tl;
  Coord<T> br;
};

template <class T>
std::ostream &operator<<(std::ostream &o, const Bounds<T> &b) {
  o << "{ " << b.tl.x << " x " << b.tl.y << " / " << b.br.x << " x " << b.br.y
    << " }";

  return o;
};

}  // namespace G13

#endif  // BOUNDS_H
