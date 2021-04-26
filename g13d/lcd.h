#ifndef LCD_H
#define LCD_H

#include <memory.h>

#include "g13.h"

namespace G13 {

class Device;

class G13_LCD {
 public:
  G13_LCD(Device &keypad);

  Device &_keypad;
  unsigned char image_buf[G13_LCD_BUF_SIZE + 8];
  unsigned cursor_row;
  unsigned cursor_col;
  int text_mode;

  void image(unsigned char *data, int size);
  void image_send() {
    image(image_buf, G13_LCD_BUF_SIZE);
  }

  void image_test(int x, int y);
  void image_clear() {
    memset(image_buf, 0, G13_LCD_BUF_SIZE);
  }

  unsigned image_byte_offset(unsigned row, unsigned col) {
    return col + (row / 8) * G13_LCD_BYTES_PER_ROW * 8;
  }

  void image_setpixel(unsigned row, unsigned col);
  void image_clearpixel(unsigned row, unsigned col);

  void write_char(char c, int row = -1, int col = -1);
  void write_string(const char *str);
  void write_pos(int row, int col);
};

}  // namespace G13

#endif  // LCD_H
