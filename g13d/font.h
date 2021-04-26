#ifndef FONT_H
#define FONT_H

#include <memory.h>

#include <memory>

namespace G13 {

class FontChar {
 public:
  static const int CHAR_BUF_SIZE = 8;
  enum FONT_FLAGS { FF_ROTATE = 0x01 };

  FontChar() {
    memset(bits_regular, 0, CHAR_BUF_SIZE);
    memset(bits_inverted, 0, CHAR_BUF_SIZE);
  }

  void set_character(unsigned char *data, int width, unsigned flags);
  unsigned char bits_regular[CHAR_BUF_SIZE];
  unsigned char bits_inverted[CHAR_BUF_SIZE];
};

class Font {
 public:
  Font();
  Font(const std::string &name, unsigned int width = 8);

  void set_character(unsigned int c, unsigned char *data);

  template <class ARRAY_T, class FLAGST>
  void install_font(ARRAY_T &data, FLAGST flags, int first = 0);

  const std::string &name() const {
    return _name;
  }
  unsigned int width() const {
    return _width;
  }

  const FontChar &char_data(unsigned int x) {
    return _chars[x];
  }

 protected:
  std::string _name;
  unsigned int _width;

  FontChar _chars[256];
};

typedef std::shared_ptr<Font> FontPtr;

}  // namespace G13

#endif  // FONT_H
