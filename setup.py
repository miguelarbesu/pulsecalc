#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""pulsecalc
A CLI for calculating RF pulse powers in NMR.
"""

import sys
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

exec(open("src/pulsecalc/_version.py").read())

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

short_description = __doc__.split("\n")

with open("README.md", "r") as handle:
    long_description = handle.read()


setup(
    name="pulsecalc",
    version=__version__,
    short_description=short_description[1],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Miguel Arbesú",
    author_email="miguelarbesu@gmail.com",
    url="https://github.com/miguelarbesu/pulsecalc",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
    include_package_data=True,
    entry_points={"console_scripts": ["pulsecalc = pulsecalc.__main__:main"]},
    license="MIT",
    setup_requires=[] + pytest_runner,
    install_requires=[
        # Basic libs
        "matplotlib>3",
        "pandas>1",
        "jupyter",
        # Extra - uncomment to use or add more
        # "scikit-learn",
        # "scikit-image",
        # "seaborn",
        # "pymc3"
    ],
    python_requires=">=3.7",
)
