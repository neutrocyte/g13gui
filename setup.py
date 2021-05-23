#!/usr/bin/python3

from setuptools import setup, find_packages
from os import path
from io import open

from g13gui.common import PROGNAME
from g13gui.common import VERSION


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PROGNAME,
    version=VERSION,
    description='A Gtk 3 application to configure the Logitech G13 gameboard',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jtgans/g13',
    author='June Tate-Gans',
    author_email='june@theonelab.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Operating System :: Linux'
    ],
    keywords='gaming',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.8.0',
    install_requires=[
        'dbus-python==1.2.16',
        'evdev==1.4.0',
        'Pillow==7.0.0',
        'PyGObject==3.40.1',
        'pyusb==1.0.2',
        'xdg==5.0.2'
    ],
    data_files={
        'share/applications': [
            path.join(here, 'com.theonelab.g13gui.Configurator.desktop'),
            path.join(here, 'com.theonelab.g13gui.applet.Clock.desktop'),
            path.join(here, 'com.theonelab.g13gui.applet.Profiles.desktop'),
        ],
        'share/icons/hicolor/scalable/apps': [
            path.join(here, 'g13-logo.svg')
        ]
    },
    entry_points={
        'console_scripts': [
            'g13gui=g13gui.main:main',
            'g13-clock=g13gui.applets.clock:main',
            'g13-profiles=g13gui.applets.profiles:main'
        ],
    },
)
