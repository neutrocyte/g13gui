#include "device.h"
#include "font.h"

using namespace std;

namespace G13 {

#include "font8x8.h"

G13_Font::G13_Font() : _name("default"), _width(8) {}

G13_Font::G13_Font(const std::string &name, unsigned int width)
    : _name(name), _width(width) {}

void G13_FontChar::set_character(unsigned char *data, int width,
                                 unsigned flags) {
  unsigned char *dest = bits_regular;
  memset(dest, 0, CHAR_BUF_SIZE);

  if (flags && FF_ROTATE) {
    for (int x = 0; x < width; x++) {
      unsigned char x_mask = 1 << x;
      for (int y = 0; y < 8; y++) {
        if (data[y] & x_mask) {
          dest[x] |= 1 << y;
        }
      }
    }
  } else {
    memcpy(dest, data, width);
  }

  for (int x = 0; x < width; x++) {
    bits_inverted[x] = ~dest[x];
  }
}

template <typename T, int size> int GetFontCharacterCount(T (&)[size]) {
  return size;
}

template <class ARRAY_T, class FLAGST>
void G13_Font::install_font(ARRAY_T &data, FLAGST flags, int first) {
  for (int i = 0; i < GetFontCharacterCount(data); i++) {
    _chars[i + first].set_character(&data[i][0], _width, flags);
  }
}

void G13_Device::_init_fonts() {
  _current_font = FontPtr(new G13_Font("8x8", 8));
  _fonts[_current_font->name()] = _current_font;

  _current_font->install_font(font8x8_basic, G13_FontChar::FF_ROTATE, 0);

  FontPtr fiveXeight(new G13_Font("5x8", 5));
  fiveXeight->install_font(font5x8, 0, 32);
  _fonts[fiveXeight->name()] = fiveXeight;
}

} // namespace G13
