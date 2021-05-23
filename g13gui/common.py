#!/usr/bin/python

from pathlib import Path
from appdirs import user_config_dir

PROGNAME = 'g13gui'
VERSION = '0.1.0'
PROFILES_CONFIG_PATH = Path(user_config_dir()) / 'g13' / 'g13gui' / 'profiles.json'
