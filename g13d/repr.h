#ifndef REPR_H
#define REPR_H

#include <string>
#include <ostream>

namespace G13 {

void string_repr_out::write_on(std::ostream &o) const {
  const char *cp = s.c_str();
  const char *end = cp + s.size();

  o << "\"";

  while (cp < end) {
    switch (*cp) {
      case '\n':
        o << "\\n";
        break;

      case '\r':
        o << "\\r";
        break;

      case '\0':
        o << "\\0";
        break;

      case '\t':
        o << "\\t";
        break;

      case '\\':
      case '\'':
      case '\"':
        o << "\\" << *cp;
        break;

      default: {
        char c = *cp;
        if (c < 32) {
          char hi = '0' + (c & 0x0f);
          char lo = '0' + ((c >> 4) & 0x0f);
          o << "\\x" << hi << lo;
        } else {
          o << c;
        }
      }
    }

    cp++;
  }

  o << "\"";
};

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
