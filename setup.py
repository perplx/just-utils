#!/usr/bin/env python3

"""Just Utils"""


# standard imports
from setuptools import setup


setup(
    name="just-utils",
    version="0.0.1",
    author="Julien Dubuc",
    author_email="",

    description="Just Utils",
    long_description="Simple, useful, self-contained python modules.",
    url="https://github.com/perplx/just-utils",
    download_url="https://github.com/perplx/just-utils/archive/refs/heads/master.zip",

    keywords="",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",  # checked using `vermin` tool
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9" ,
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],

    packages=["just"],
    package_dir={"": "src"},
    package_data={"just": ["py.typed"]},

    setup_requires=[],
    install_requires=[],
    extras_require={
        # black is pinned: its stable style changes yearly and newer majors drop older Pythons,
        # so an unpinned install formats inconsistently across the supported Python range (see tests.yml)
        "dev": ["black<26", "flake8", "mypy", "pytest-cov", "vermin"],
        "docs": ["sphinx", "sphinx-autodoc-typehints", "sphinx-mdinclude", "python_docs_theme"],
        "types": ["types-setuptools"],
    },

    test_suite="tests",
)
