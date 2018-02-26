#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import sys
from io import open

from setuptools import find_packages, setup

try:
    from pypandoc import convert_file

    def read_md(f):
        return convert_file(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")

    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()


version = '1.3.0'


setup(
    name='django-crmify',
    version=version,
    url='https://github.com/MeanPug/django-crmify',
    license='Apache License 2.0',
    description='Connect your Django Application to your CRM of choice',
    long_description=read_md('README.md'),
    author='Bobby Steinbach',
    author_email='developers@meanpug.com',
    packages=find_packages(exclude=['tests*', 'examples*']),
    include_package_data=True,
    install_requires=[
        'requests>=2.18,<2.19'
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
