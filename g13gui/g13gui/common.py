#!/usr/bin/python

import os
import os.path
import xdg.BaseDirectory as basedir

VERSION = '0.1.0'
PROFILES_CONFIG_PATH = os.path.join(basedir.save_config_path('g13', 'g13gui'),
                                    'profiles.json')
