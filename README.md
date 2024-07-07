Just Utils
==========

Simple, useful, self-contained python modules.

[![tests](https://github.com/perplx/just-utils/actions/workflows/tests.yml/badge.svg?event=push)](https://github.com/perplx/just-utils/actions/workflows/tests.yml)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/perplx/37049f20166246459e2d38ee8ddf2afe/raw/just-utils_master.json)](https://github.com/perplx/just-utils/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Features
========

Every module is found in the `just` package.

- The module `just.args` provides command-line argument parsers for common types of command-line arguments: dates, directory-paths, log-levels. These are functions or objects which can be used as the `type=` argument for an argument parsed using the standard `argparse` module. The parsers will perform the necessary checking and show any parsing problems as command-line errors.
- The module `just.deprecate` provides the `@deprecated` decorator to mark functions as deprecated. The standard `warnings` module will emit a `DeprecationWarning` whenever such a function is used at run-time.
- The module `just.heap` provides the class `Heap`, which imprements a priority-heap using the functions in the standard `heapq` module. The class can use the values themselves as a priority, or use a provided key-function to compute it.
- The module `just.lock` provides a way to lock a section of code by using a simple lock-file. It provides a context-manager that will abort when trying to acquire an already-locked file.
- The module `just.timing` provides ways to conveniently time the execution of a block of code, using context-managers or decorators. The timing information can be shown on the console or in a provided `Logger` object.

Each module has corresponding unit-tests, and contains api-documentation that can be generated using [Sphinx](https://www.sphinx-doc.org/en/master/index.html)

Install
=======

```shell
pip install $just_util_dir
```

There are no dependencies to install.

API Documentation
-----------------

The tools needed to generate the API documentation can be installed using the optional `[docs]` argument to `pip`:

```shell
pip install $just_util_dir[docs]
```

This will install Sphinx as well as all the related modules referenced in the docs configuration.

Optional Features
-----------------

These are some extra features that can be installed using the optional `[extra]` argument to `pip`:

```shell
pip install $just_util_dir[extra]
```

The extras installed will be:

package                                                | description
-------------------------------------------------------|-----------------------------------
[black](https://pypi.org/project/black/)               | uncompromising code formatter
[flake8](https://pypi.org/project/flake8/)             | checks code quality
[mypy](https://pypi.org/project/mypy/)                 | static type checking
[pytest-cov](https://pypi.org/project/pytest-cov/)     | run unit tests and test coverage
[vermin](https://pypi.org/project/vermin/)             | determine minimum python version

Config Files
============

There are some configuration files for some optional tools:

file                               | description
-----------------------------------|-----------------------------------
[.editorconfig](.editorconfig)     | configuration file for for [EditorConfig](https://editorconfig.org/)
[pyproject.toml](pyproject.toml)   | contains configuration for [black](https://pypi.org/project/black/)
[setup.cfg](setup.cfg)             | contains configuration for [flake8](https://pypi.org/project/flake8/)
