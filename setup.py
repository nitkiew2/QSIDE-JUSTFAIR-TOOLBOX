#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 15:01:53 2023

@author: jason
"""

from setuptools import find_packages
from setuptools import setup

setup(
    name='JUSTFAIR_Tools',
    version='0.1dev',
    packages= ['JUSTFAIR_Tools'],
    license='General Public License 3.0',
    install_requires = ['matplotlib']
    #long_description=open('README.md').read(),
)
