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
        "Programming Language :: Python :: 3.6"  # checked using `vermin` tool
        "Topic :: Utilities",
    ],

    packages=["just"],
    package_dir={"": "src"},
    package_data={"just": ["py.typed"]},

    setup_requires=[],
    install_requires=[],
    extras_require={
        "dev": ["black", "flake8", "mypy", "pytest-cov", "vermin"],
        "docs": ["sphinx", "sphinx-autodoc-typehints", "sphinx-mdinclude", "python_docs_theme"],
        "types": ["types-setuptools"],
    },

    test_suite="tests",
)
