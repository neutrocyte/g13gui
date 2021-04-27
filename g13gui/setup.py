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
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
    ],
    keywords='gaming',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5.0',
    install_requires=[
        'gi',
    ],
    package_data={
    },
    entry_points={
        'console_scripts': [
            'g13gui=g13gui.main:main',
        ],
    },
)
