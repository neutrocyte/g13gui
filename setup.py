#!/usr/bin/python3

from setuptools import setup, find_packages
from os import path
from io import open


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='g13gui',
    version='0.1.0',
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
    python_requires='>=3.5.0',
    install_requires=[
        'PyGObject',
        'PIL',
        'Xlib',
        'dbus',
        'evdev',
        'gzip',
        'usb'
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
            'g13-clock=g13gui.applets.clock:',
            'g13-profiles=g13gui.applets.profiles:'
        ],
    },
)
