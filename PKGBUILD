# Maintainer: June Tate-Gans <june@theonelab.com>

pkgbase="g13gui"
pkgname="g13gui-git"
pkgver=d4a5186
pkgrel=1
pkgdesc="A user-space driver and GUI configurator for the Logitech G13"
arch=('any')
url="https://github.com/jtgans/g13gui"
license=('BSD')
depends=(
  'python>=3.8'
  'python-evdev'
  'python-pyusb>=1.0.2'
  'python-dbus'
  'python-gobject'
  'python-pyusb'
  'python-pillow>=10.0.1'
  'python-cffi'
  'python-psutil'
  'python-appdirs'
  'xorg-fonts-misc'
)
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
