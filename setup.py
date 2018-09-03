# -*- coding： utf-8 -*-
# author：pengr
from __future__ import print_function
from setuptools import setup, find_packages
import sys
 
setup(
    name="simple-spiders",
    version="0.0.1",
    author="Pengr",
    author_email="pengrui55555@163.com",
    description="A simple web crawling framework.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/duiliuliu/simple-spiders",
    packages=['tidypage'],
    install_requires=[
        "requests",
        "lxml",
        "csv",
        "xlwt",
        "xlsxwriter"
        ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Natural Language :: Chinese (Simplified)',
        'Topic :: Communications :: Email',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Internet',
        'Topic :: Software Development :: Version Control :: Git',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
    ],
)
