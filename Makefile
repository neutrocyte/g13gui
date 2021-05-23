VERSION   := `grep "VERSION" g13gui/common.py |awk '{ print $$2 }' |sed 's/'//g'`
GITBRANCH ?= master
PIPENV    := pipenv
PYTHON    := `which python3`
PIP       := $(PYTHON) -m pip


all:
	export GITBRANCH=master
	debuild
	debclean

build:
	gbp buildpackage --git-debian-branch=$(GITBRANCH)

clean:
	debclean

build-source: clean
	gbp buildpackage -S --git-debian-branch=$(GITBRANCH)
	mkdir build
	mv ../g13gui_$(VERSION)* build

release: build-source
