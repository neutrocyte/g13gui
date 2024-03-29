#!/bin/bash
#
# Bare-minimum shell script to isolate distro-specific setup requirements
# without using make, which has been a standard part of POSIX for decades,
# but for some idiotic reason not installed on Linux images by default.

die() {
	echo "$@" >/dev/stderr
	exit 1
}

try() {
	echo "$@"
	"$@" || die "error: $1 exited with code $?"
}

DISTRO="$1"; shift

[[ -z "${DISTRO}" ]] && die "Usage: dockerbuild.sh <distro>"

case "${DISTRO}" in
	archlinux)
		try pacman -Sy --noconfirm
		try pacman -S --noconfirm base-devel python meson lsb-release git

		# Work around makepkg brain-damage and build as nobody
		try mkdir -p /tmp/build
		try cp -r /srcs /tmp/build
		try chown -R nobody:nobody /tmp/build
		cd /tmp/build
		try sudo -u nobody make
		try cp build/* /srcs/build
		;;

	debian)
		# Work around pbuilder brain-damage in noninteractive contexts.
		try touch /etc/pbuilderrc
		try apt-get update
		try apt-get install -y devscripts build-essential git-buildpackage appstream dh-sequence-python3 meson
		cd /srcs
		try make
		;;

	fedora)
		try dnf install -y rpmdevtools rpmlint make python meson lsb-release git
		cd /srcs
		try make
		;;

	*)
		die "Unknown distro '${DISTRO}'."
esac

