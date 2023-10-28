# Maintainer: June Tate-Gans <june@theonelab.com>

pkgbase="g13gui"
pkgname="g13gui-git"
pkgver=fa65c30
pkgrel=1
pkgdesc="A user-space driver and GUI configurator for the Logitech G13"
arch=('any')
url="https://github.com/jtgans/g13gui"
license=('GPL')
depends=('python' 'python-evdev' 'python-pyusb', 'xorg-fonts-misc')
makedepends=('git' 'meson')
source=("${pkgname}::git+http://github.com/jtgans/g13gui.git")
sha256sums=('SKIP')

pkgver() {
    cd "${srcdir}"
    git rev-parse --short HEAD
}

prepare() {
    cd "${srcdir}"
    git checkout master
}

build() {
    arch-meson "${srcdir}/${pkgname}" build
}

package() {
    meson install -C build --destdir "${pkgdir}"
}