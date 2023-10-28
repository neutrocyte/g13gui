VERSION   := `grep "VERSION" g13gui/common.py |awk '{ print $$2 }' |sed 's/'//g'`
GITBRANCH ?= master
PIPENV    := pipenv
PYTHON    := `which python3`
PIP       := ${PYTHON} -m pip

DISTRO    := $(shell \
    lsb_release -i \
        |awk -F: '{ print $$2 }' \
        |sed -e 's/[ \t]*//g' \
        |tr '[A-Z]' '[a-z]' \
        |sed -e 's/linux//g')

$(warning Building on ${DISTRO})

all: ${DISTRO}

clean: ${DISTRO}-clean

install: ${DISTRO}-install

manjaro:
	makepkg

manjaro-clean:
	rm -f g13gui-git-*-any.pkg.tar.zst
	rm -rf g13gui-git/
	rm -rf pkg/
	rm -rf src/

manjaro-install:
	makepkg -i

debian:
	export GITBRANCH=master
	debuild
	debclean

debian-build:
	gbp buildpackage --git-debian-branch=$(GITBRANCH)

debian-clean:
	debclean

debian-build-source: debian-clean
	gbp buildpackage -S --git-debian-branch=$(GITBRANCH)
	mkdir build
	mv ../g13gui_$(VERSION)* build

debian-release: debian-build-source
