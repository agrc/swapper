#!/usr/bin/env python
# * coding: utf8 *
"""
setup.py
A module that installs swapper as a module
"""

from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="swapper",
    version="1.1.0",
    license="MIT",
    description="Move data from one SDE database to another with minimal downtime",
    author="Zach Beck",
    author_email="zbeck@utah.gov",
    url="https://github.com/agrc/swapper",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    project_urls={
        "Issue Tracker": "https://github.com/agrc/swapper/issues",
    },
    keywords=["gis"],
    install_requires=[
        "docopt==0.*",
        "python-dotenv==1.*",
        "pyodbc==5.*",
        "xxhash==3.*",
    ],
    extras_require={
        "tests": [
            "pytest-cov==5.*",
            "pytest-instafail==0.5.*",
            "pytest-mock==3.*",
            "pytest-ruff==0.*",
            "pytest-watch==4.*",
            "pytest==8.*",
            "black==24.*",
            "ruff==0.*",
        ]
    },
    setup_requires=[
        "pytest-runner",
    ],
    entry_points={"console_scripts": ["swapper = swapper.__main__:main"]},
)
