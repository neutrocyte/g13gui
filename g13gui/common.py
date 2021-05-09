#!/usr/bin/python

import os
import os.path
import xdg.BaseDirectory as basedir

PROGNAME = 'g13gui'
VERSION = '0.1.0'
PROFILES_CONFIG_PATH = os.path.join(basedir.save_config_path('g13', 'g13gui'),
                                    'profiles.json')
