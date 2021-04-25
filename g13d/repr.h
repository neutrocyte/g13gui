#ifndef REPR_H
#define REPR_H

#include <string>
#include <ostream>

namespace G13 {

struct string_repr_out {
  string_repr_out(const std::string &str) : s(str) {}
  void write_on(std::ostream &) const;

  std::string s;
};

inline std::ostream &operator<<(std::ostream &o, const string_repr_out &sro) {
  sro.write_on(o);
  return o;
}

template <class T> inline const T &repr(const T &v) {
  return v;
}

inline string_repr_out repr(const char *s) {
  return string_repr_out(s);
}

inline string_repr_out repr(const std::string &s) {
  return string_repr_out(s);
}

}

#endif // REPR_H
