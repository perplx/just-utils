#!/usr/bin/env python3

"""Just Utils"""


# standard imports
import os
from setuptools import setup


def read(file_name):
    """Utility function to read the README file.
    Used for the long_description in setuptools.setup().
    """

    file_path = os.path.join(os.path.dirname(__file__), file_name)
    return open(file_path).read()


setup(
    name = "just-utils",
    version = "0.0.1",
    author = "Julien Dubuc",
    author_email = "",

    description = "Just Utils",
    long_description = read("README.md"),
    url = "https://github.com/perplx/just-utils",
    download_url="https://github.com/perplx/just-utils/archive/refs/heads/master.zip",

    keywords = "",
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6"  # checked using `vermin` tool
        "Topic :: Utilities",
    ],

    packages = ["just"],
    setup_requires = [],
    install_requires = [],
    extras_require = {"extra": ["black", "vermin"]},

    test_suite = "tests",
)
