#!/usr/bin/env python
# * coding: utf8 *
'''
setup.py
A module that installs swapper as a module
'''

from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="swapper",
    version="1.0.0",
    license="MIT",
    description="Move data from one SDE database to another with minimal downtime",
    author="Zach Beck",
    author_email="zbeck@utah.gov",
    url="https://github.com/agrc/swapper",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
    project_urls={
        'Issue Tracker': 'https://github.com/agrc/swapper/issues',
    },
    keywords=['gis'],
    install_requires=[
        'docopt==0.6.*',
        'python-dotenv>=0.10,<1.1',
        'pyodbc>=4.0,<5.1',
        'xxhash>=3.*'
    ],
    extras_require={
        'tests': [
            'pylint-quotes==0.2.*',
            'pylint>=2.5,<3.1',
            'pytest-cov>=2.9,<4.2',
            'pytest-instafail>=0.4,<0.6',
            'pytest-isort>=1.0,<3.2',
            'pytest-pylint>=0.17,<0.22',
            'pytest-watch==4.2.*',
            'pytest>=5.4,<7.5',
            'yapf>=0.30,<0.41',
        ]
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        "console_scripts": [
            "swapper = swapper.__main__:main"
        ]
    }
)
