CXXFLAGS  := $(CXXFLAGS) -DBOOST_LOG_DYN_LINK=1 -std=c++0x
LIBS      := -lusb-1.0 -lboost_program_options -lboost_log -lboost_system -lpthread
PREFIX    ?= /usr/local

G13D_SRCS := \
	g13d/g13.cc \
	g13d/g13_fonts.cc \
	g13d/g13_keys.cc \
	g13d/g13_lcd.cc \
	g13d/g13_log.cc \
	g13d/g13_main.cc \
	g13d/g13_stick.cc \
	g13d/helper.cc

G13D_OBJS := $(patsubst g13d/%.cc,build/%.o,$(G13D_SRCS))

all: build build/g13d build/pbm2lpbm

build:
	mkdir -p build

build/g13d: $(G13D_OBJS) | build
	$(CXX) $(G13D_OBJS) -o build/g13d $(LIBS)

build/pbm2lpbm: src/pbm2lpbm.c | build
	$(CXX) $(CXXFLAGS) src/pbm2lpbm.c -o build/pbm2lpbm

build/%.o: src/%.cc
	$(CXX) -c -o $@ $< $(CXXFLAGS)

clean: 
	rm -rf build

install: build/g13d build/pbm2lpbm
	install -d ${HOME}/.local/bin
	install -m700 -d ${HOME}/.local/var/g13d
	install -d ${HOME}/.config/systemd/user
	cat etc/g13d.service |sed "s,@HOME@,${HOME},g" > ${HOME}/.config/systemd/user/g13d.service
	install -m755 build/g13d ${HOME}/.local/bin/g13d
	install -m755 build/pbm2lpbm ${HOME}/.local/bin/pbm2lpbm

.PHONY: all clean install
