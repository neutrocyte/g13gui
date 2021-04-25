#ifndef G13_H
#define G13_H

#include <boost/log/trivial.hpp>

#include <string>

namespace G13 {

#define G13_LOG(level, message) BOOST_LOG_TRIVIAL(level) << message
#define G13_OUT(message) BOOST_LOG_TRIVIAL(info) << message

const size_t G13_INTERFACE = 0;
const size_t G13_KEY_ENDPOINT = 1;
const size_t G13_LCD_ENDPOINT = 2;
const size_t G13_KEY_READ_TIMEOUT = 0;
const size_t G13_VENDOR_ID = 0x046d;
const size_t G13_PRODUCT_ID = 0xc21c;
const size_t G13_REPORT_SIZE = 8;
const size_t G13_LCD_BUFFER_SIZE = 0x3c0;
const size_t G13_NUM_KEYS = 40;

const size_t G13_LCD_COLUMNS = 160;
const size_t G13_LCD_ROWS = 48;
const size_t G13_LCD_BYTES_PER_ROW = G13_LCD_COLUMNS / 8;
const size_t G13_LCD_BUF_SIZE = G13_LCD_ROWS * G13_LCD_BYTES_PER_ROW;
const size_t G13_LCD_TEXT_CHEIGHT = 8;
const size_t G13_LCD_TEXT_ROWS = 160 / G13_LCD_TEXT_CHEIGHT;

enum stick_mode_t {
  STICK_ABSOLUTE,
  STICK_RELATIVE,
  STICK_KEYS,
  STICK_CALCENTER,
  STICK_CALBOUNDS,
  STICK_CALNORTH
};

typedef int LINUX_KEY_VALUE;
const LINUX_KEY_VALUE BAD_KEY_VALUE = -1;

typedef int G13_KEY_INDEX;

class G13_CommandException : public std::exception {
public:
  G13_CommandException(const std::string &reason) : _reason(reason) {}
  virtual ~G13_CommandException() throw() {}
  virtual const char *what() const throw() { return _reason.c_str(); }

  std::string _reason;
};

} // namespace G13

#endif // __G13_H__
