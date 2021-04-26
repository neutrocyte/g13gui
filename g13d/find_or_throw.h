#ifndef FIND_OR_THROW_H
#define FIND_OR_THROW_H

#include <map>

namespace G13 {

class NotFoundException : public std::exception {
 public:
  const char *what() throw();
};

template <class K_T, class V_T>
inline const V_T &find_or_throw(const std::map<K_T, V_T> &m,
                                const K_T &target) {
  auto i = m.find(target);

  if (i == m.end()) {
    throw NotFoundException();
  }

  return i->second;
};

template <class K_T, class V_T>
inline V_T &find_or_throw(std::map<K_T, V_T> &m, const K_T &target) {
  auto i = m.find(target);

  if (i == m.end()) {
    throw NotFoundException();
  }

  return i->second;
};

}  // namespace G13

#endif  // FIND_OR_THROW_H
