#! /usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'ipap - Image Processing and Analysis Project',
    'author': 'Magnus Bjerke Vik, Thomas Mellemseter',
    'url': 'https://github.com/ipapi/ipap',
    'author_email': 'mbvett@gmail.com',
    'version': '0.1',
    'install_requires': [''],
    'packages': ['ipap'],
    'scripts': [],
    'name': 'ipap',
    'license': 'GPL'
}

setup(**config)
