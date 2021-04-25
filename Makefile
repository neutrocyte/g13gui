all: g13d pbm2lpbm

FLAGS=$(CXXFLAGS) -DBOOST_LOG_DYN_LINK -std=c++0x
LIBS=-lusb-1.0 -lboost_log -lboost_log_setup-mt -lboost_thread -lboost_system-mt -lpthread

g13.o: g13.h helper.hpp g13.cc
	g++ $(FLAGS) -c g13.cc

g13_main.o: g13.h helper.hpp g13_main.cc
	g++ $(FLAGS) -c g13_main.cc


g13_log.o: g13.h helper.hpp g13_log.cc
	g++ $(FLAGS) -c g13_log.cc

g13_fonts.o: g13.h helper.hpp g13_fonts.cc
	g++ $(FLAGS) -c g13_fonts.cc

g13_lcd.o: g13.h helper.hpp g13_lcd.cc
	g++ $(FLAGS) -c g13_lcd.cc

g13_stick.o: g13.h helper.hpp g13_stick.cc
	g++ $(FLAGS) -c g13_stick.cc

g13_keys.o: g13.h helper.hpp g13_keys.cc
	g++ $(FLAGS) -c g13_keys.cc

helper.o: helper.hpp helper.cpp
	g++ $(FLAGS) -c helper.cpp


g13d: g13_main.o g13.o g13_log.o g13_fonts.o g13_lcd.o g13_stick.o g13_keys.o helper.o
	g++ -o g13d -std=c++0x \
		g13_main.o g13.o g13_log.o g13_fonts.o g13_lcd.o g13_stick.o g13_keys.o helper.o \
	 	-lusb-1.0 -lboost_program_options \
	 	-lboost_log    \
	 	-lboost_system -lpthread

pbm2lpbm: pbm2lpbm.c
	g++ -o pbm2lpbm pbm2lpbm.c

clean: 
	rm -f g13 pbm2lpbm

install:
	install -d ${HOME}/.local/bin
	install -m700 -d ${HOME}/.local/var/g13d
	install -d ${HOME}/.config/systemd/user
	cat g13d.service |sed "s,@HOME@,${HOME},g" > ${HOME}/.config/systemd/user/g13d.service
	install -m755 g13d ${HOME}/.local/bin/g13d

.PHONY: all clean install
