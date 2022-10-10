Just Utils
==========

Simple, useful, self-contained modules.

[![tests](https://github.com/perplx/just-utils/actions/workflows/tests.yml/badge.svg)](https://github.com/perplx/just-utils/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Install
=======

```shell
pip install $just_util_dir
```

There are no dependencies to install.

Optional Features
-----------------

These are some extra features installed using the optional `[extra]` argument to `pip`:

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

Scripts
=======

There are some shell scripts to run the optional tools:

file                               | description
-----------------------------------|-----------------------------------
[run_black.sh](run_black.sh)       | runs `black` on the source code, *modifies it in place!*
[run_coverage.sh](run_coverage.sh) | runs `coverage` on the source code, shows unit test results and coverage
[run_flake8.sh](run_flake8.sh)     | runs `flake8` on the source code, shows code quality erros
[run_mypy.sh](run_mypy.sh)         | runs `mypy` on the source code, shows type errors
[run_vermin.sh](run_vermin.sh)     | runs `vermin` on the source code, shows minimum python version

These assume the tools are installed in the current python environment
