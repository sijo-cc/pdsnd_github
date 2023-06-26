# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='divy-us-bikeshare-data',
    version='0.4.0',
    description='Divy US Bikeshare Data',
    author='Sijo Jose',
    author_email='',
    url="",
    packages=find_packages(exclude=['tests*']),
    py_modules=['cli'],
    install_requires=[
        'click>=7.0',
    ],
    entry_points='''
    [console_scripts]
    bike_data=tools.cli:bike_share_interactive
    ''',
)

