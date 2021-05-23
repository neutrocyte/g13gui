project(
  'lutris',
  license: 'MIT'
)

python = import('python').find_installation()

prefix = get_option('prefix')
bindir = get_option('bindir')
etcdir = get_option('etcdir')
g13dir = join_paths(pylibdir, 'g13gui')

install_data(
  files('bin/g13gui', 'bin/g13-clock', 'bin/g13-profiles'),
  install_dir: bindir,
  install_mode: 'rwxr-xr-x',
)

install_subdir(
  'g13gui',
  install_dir: pylibdir,
)

install_data(
  files('etc/g13-logo.svg'),
  install_dir: join_paths(datadir, 'icons/hicolor/scalable/apps'),
  install_mode: 'rw-r--r--',
)

install_data(
  files('etc/com.theonelab.g13gui.Configurator.desktop',
        'etc/com.theonelab.g13gui.applet.Clock.desktop',
        'etc/com.theonelab.g13gui.applet.Profiles.desktop'),
  install_dir: join_paths(datadir, 'applications'),
  install_mode: 'rw-r--r--',
)

install_data(
  files('etc/91-g13.rules'),
  install_dir: join_paths(etcdir, 'udev/rules.d'),
  install_mode: 'rw-r--r--',
)
