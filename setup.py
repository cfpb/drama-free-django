#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name = "no-drama",
    version = "2.0",
    packages = find_packages(),
    include_package_data = True,
    entry_points={
        'console_scripts':[
            'no-drama=no_drama.cli:main'
        ]
    },
    install_requires=[
        'jinja2>=2.9.5',
    ],
    test_suite='tests',
)
