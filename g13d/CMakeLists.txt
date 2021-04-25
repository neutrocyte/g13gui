cmake_minimum_required(VERSION 3.16.3)

project(g13d CXX)
add_executable(pbm2lpbm pbm2lpbm.cc)
add_executable(g13d
  g13.cc
  g13_fonts.cc
  g13_keys.cc
  g13_lcd.cc
  g13_log.cc
  g13_main.cc
  g13_stick.cc
  helper.cc
)

target_compile_definitions(g13d PUBLIC BOOST_LOG_DYN_LINK=1)
find_package(PkgConfig)
pkg_check_modules(libusb-1.0 REQUIRED libusb-1.0)
find_package(Boost REQUIRED COMPONENTS system log program_options)

target_link_libraries(g13d
  ${Boost_SYSTEM_LIBRARY} ${Boost_LOG_LIBRARY} ${Boost_PROGRAM_OPTIONS_LIBRARY}
  ${libusb-1.0_LIBRARIES})

install(TARGETS g13d pbm2lpbm RUNTIME)
