#ifndef COORD_H
#define COORD_H

namespace G13 {

template <class T>
class Coord {
 public:
  Coord() : x(), y() {
  }

  Coord(T _x, T _y) : x(_x), y(_y) {
  }

  T x;
  T y;
};

template <class T>
std::ostream &operator<<(std::ostream &o, const Coord<T> &c) {
  o << "{ " << c.x << " x " << c.y << " }";
  return o;
};

}  // namespace G13

#endif  // COORD_H
