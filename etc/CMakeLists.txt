cmake_minimum_required(VERSION 3.16.3)
project(g13)

install(FILES 91-g13.rules DESTINATION /etc/udev/rules.d)
install(FILES g13d.service DESTINATION /lib/systemd/system)
