#!/usr/bin/python

from xdg import xdg_config_home

PROGNAME = 'g13gui'
VERSION = '0.1.0'
PROFILES_CONFIG_PATH = xdg_config_home() / 'g13' / 'g13gui' / 'profiles.json'
