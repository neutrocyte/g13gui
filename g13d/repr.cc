#include <ostream>

#include "repr.h"

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

} // namespace G13
