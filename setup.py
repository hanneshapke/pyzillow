#!/usr/bin/env python
#

"""

Distutils setup script for pyzillow.

"""


import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

readme = open("README.rst").read()
doclink = """
Documentation
-------------

The full documentation is at https://pyzillow.readthedocs.io/."""
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

setup(
    name="pyzillow",
    version="0.7.0",
    description="Python API wrapper for Zillow's API",
    long_description=readme + "\n\n" + doclink + "\n\n" + history,
    author="Hannes Hapke",
    author_email="hannes.hapke@gmail.com",
    url="https://github.com/hanneshapke/pyzillow",
    packages=["pyzillow"],
    package_dir={"pyzillow": "pyzillow"},
    include_package_data=True,
    install_requires=["requests"],
    license="MIT",
    zip_safe=False,
    keywords=["pyzillow", "zillow", "api", "real estate"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
