/*
 * helper.hpp
 *
 * Miscellaneous helpful little tidbits...
 */

/*
 * Copyright (c) 2015, James Fowler
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files
 * (the "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to permit
 * persons to whom the Software is furnished to do so, subject to the
 * following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 */

#ifndef HELPER_HPP
#define HELPER_HPP

#include <boost/algorithm/string.hpp>
#include <boost/foreach.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/seq.hpp>
#include <boost/shared_ptr.hpp>
#include <exception>
#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <vector>

namespace Helper {

template <class MAP_T>
struct _map_keys_out {
  _map_keys_out(const MAP_T &c, const std::string &s) : container(c), sep(s) {
  }

  const MAP_T &container;
  std::string sep;
};

template <class STREAM_T, class MAP_T>
STREAM_T &operator<<(STREAM_T &o, const _map_keys_out<MAP_T> &_mko) {
  bool first = true;
  for (auto i = _mko.container.begin(); i != _mko.container.end(); i++) {
    if (first) {
      first = false;
      o << i->first;
    } else {
      o << _mko.sep << i->first;
    }
  }
  return o;
};

template <class MAP_T>
_map_keys_out<MAP_T> map_keys_out(const MAP_T &c,
                                  const std::string &sep = " ") {
  return _map_keys_out<MAP_T>(c, sep);
};

};  // namespace Helper

#endif  // HELPER_HPP
