cmake_minimum_required(VERSION 3.16.3)
project(g13d LANGUAGES CXX VERSION "0.1.0")

configure_file("config.h.in" "config.h")
include_directories(${CMAKE_CURRENT_BINARY_DIR})

set(CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "Configs" FORCE)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Werror")

add_executable(pbm2lpbm pbm2lpbm.cc)
add_executable(g13d
  action.cc
  device.cc
  font.cc
  g13_keys.cc
  g13_lcd.cc
  g13_main.cc
  g13_stick.cc
  helper.cc
  manager.cc
)

target_compile_definitions(g13d PRIVATE BOOST_LOG_DYN_LINK=1)

find_package(PkgConfig)
pkg_check_modules(libusb-1.0 REQUIRED libusb-1.0)
find_package(Boost REQUIRED COMPONENTS system log program_options)

target_link_libraries(g13d
  ${Boost_SYSTEM_LIBRARY} ${Boost_LOG_LIBRARY} ${Boost_PROGRAM_OPTIONS_LIBRARY}
  ${libusb-1.0_LIBRARIES})

install(TARGETS g13d pbm2lpbm RUNTIME)
install(CODE "
  execute_process(COMMAND install -d -m 0660 -o root -g input /run/g13d)
  message(STATUS \"Install: /run/g13d\")
")
