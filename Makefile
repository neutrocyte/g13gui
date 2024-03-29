VERSION   := `grep "VERSION" g13gui/common.py |awk '{ print $$3 }' |tr -d "'"`
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

ifeq (${DISTRO},ubuntu)
DISTRO := debian
endif

ifeq (${DISTRO},arch)
DISTRO := manjaro
endif

$(warning Building on ${DISTRO})

all: ${DISTRO}

clean: ${DISTRO}-clean
	rm -rf build/
	rm -rf env/

install: ${DISTRO}-install

manjaro:
	mkdir -p build
	makepkg -s
	mv g13gui*.pkg.tar.zst build

manjaro-clean:
	rm -f g13gui-git-*-any.pkg.tar.zst
	rm -rf g13gui-git/
	rm -rf pkg/
	rm -rf src/

manjaro-install:
	makepkg -i

debian:
	mkdir -p build
	gbp buildpackage --git-verbose --git-ignore-branch --git-debian-branch=$(GITBRANCH) -us -ui -uc
	mv ../g13gui_$(VERSION)* build

debian-install:
	sudo dpkg -i g13gui_$(VERSION).deb

debian-clean:
	debclean

debian-build-source: debian-clean
	mkdir -p build
	gbp buildpackage -S --git-verbose --git-ignore-branch --git-debian-branch=$(GITBRANCH) -us -uc
	mv ../g13gui_$(VERSION)* build

debian-release: debian-build-source

env:
	python3 -m venv env
	tools/in-env python3 -m pip install pipenv
	tools/in-env python3 -m pipenv sync --dev

test: env
	PYTHONPATH=. tools/in-env python3 -m g13gui.tests

lock: env
	tools/in-env python3 -m pipenv lock

.PHONY: all clean install
.PHONY: manjaro manjaro-clean manjaro-install
.PHONY: debian debian-build debian-clean debian-build-source debian-release

