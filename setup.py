#!/usr/bin/env python
#
# Hannes Hapke - Santiago, Chile - 2014
#
# This program is free software: MIT license 

"""
Distutils setup script for pyzillow.

"""


import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from __version__ import VERSION

setup(
    name='pyzillow',
    version=VERSION,
    author='Hannes Hapke',
    author_email='hannes@renooble.com',
    url='https://github.com/hanneshapke/pyzillow',
    download_url='https://github.com/hanneshapke/pyzillow/archive/master.zip',
    description='Python interface for Zillow\'s API. Currently supporting GetDeepSearchResults and GetUpdatedPropertyDetails API.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r').read(),
    py_modules=['pyzillow', 'pyzillowerrors', '__version__'],
    provides=['pyzillow'],
    requires=['requests'],
    install_requires=['requests >= 2.2.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='zillow real estate rental xml api address zipcode',
    license='MIT',
)