Plan
====

Proposed additions to `just-utils`: new modules, and extensions to existing ones.

Every item is meant to fit the house style: standard-library only, full type annotations,
Sphinx `:param:` docstrings with an `ex::` block, a `main()` demo, and a matching
`unittest` file in [tests/](tests/). Each module should teach one technique well, since
this repo doubles as a reference for how to write good python.

Top Picks
=========

The biggest gap-to-effort ratio; these are the ones to do first.

`just.retry`
------------

A `@retry(exceptions=..., tries=3, delay=0.5, backoff=2.0, jitter=True, logger=...)` decorator,
plus a `retrying()` context-manager / iterator form.

Nothing in the standard library does this, and everyone rewrites it badly.

Demonstrates: decorator factories, `time.monotonic` vs `time.time`, exception filtering,
and *why* jitter matters. Pairs naturally with the existing decorator patterns in
[just.timing](src/just/timing.py) and [just.deprecate](src/just/deprecate.py).

`just.human`
------------

`format_bytes(n)` -> `"10.5 MiB"`, `format_duration(s)` -> `"1h 02m 03s"`,
and the inverses `parse_bytes("10MB")` / `parse_duration("1h30m")`.

Small, pure, trivially testable, and it feeds two other modules: `just.timing` should print
`1m 03s` instead of `63.000 seconds`, and `just.args` gets `ByteSizeArg` / `TimeDeltaArg` for free.

Demonstrates: round-trip property testing (`parse(format(x)) == x`).

`just.atomic`
-------------

`with atomic_write(path) as f:` — writes to a temporary file in the same directory and
`os.replace()`s it into place on clean exit, discarding it on exception.

A genuine standard-library gap, and a *correctness* lesson: same-filesystem temp file,
`os.replace` atomicity, `fsync` before rename, cleanup in `finally`.
Conceptually the sibling of [just.lock](src/just/lock.py).

`just.log`
----------

One-call `setup_logging(level, file_path=None)` (console plus optional rotating file),
an ANSI `ColorFormatter` that degrades when `not sys.stderr.isatty()` and honours `NO_COLOR`,
and a custom `TRACE` level.

The natural other half of `args.LogLevelArg`; half the existing modules already take a
`logger=` parameter.

`just.iters`
------------

`chunked`, `sliding_window`, `flatten`, `unique_everseen`, `partition`, `take`.

`itertools.batched` only landed in 3.12, so this stays useful across the whole supported range.

Demonstrates: lazy generators, `islice`, and the "don't materialise the iterable" discipline.

Extensions to Existing Modules
==============================

`just.first`
------------

The two `# FIXME raise IndexError if none are found?` comments point at the right redesign:
a single `first(iterable, condition=None, *, default=_MISSING)` that raises `ValueError` when
no default is supplied, mirroring `next()`.

The sentinel-object idiom (`_MISSING = object()`) is exactly the kind of thing this repo exists
to record, since `None` is a legitimate value.

Then add:

- `last()`
- `only()` — returns the single element, raises if zero or two-or-more elements.
  The most-reached-for of the three, and it doesn't exist anywhere.

`just.timing`
-------------

Three things:

1. Kill the `@timed` vs `@timed()` FIXME at [timing.py:16](src/just/timing.py#L16) using the
   `callable(arg)` trick already written in [deprecate.py:64](src/just/deprecate.py#L64).
   Same problem, same solution, two modules apart — worth unifying.
2. Replace both the decorator and the context-manager with one `Timer(contextlib.ContextDecorator)`
   class that works as `with Timer(...)` *and* `@Timer(...)`, and exposes `.elapsed` afterwards so
   callers can assert on the number instead of scraping stdout. `ContextDecorator` is an underused
   standard-library gem and this is the textbook case for it.
3. The context-manager doesn't record the time if the body raises — the `yield` should be in a
   `try/finally`, the way `lock_file` already does it.

`just.open`
-----------

- Add `.xz` / `.lzma` (standard library) and `.zip`.
- Replace the `if`-chain with an extension-to-opener registry dict, so adding a format is one line.
- Add a `**kwargs` passthrough for `encoding` / `newline`.
- Add a `sniff_open()` variant that dispatches on magic bytes rather than the filename,
  for when the extension lies.

`just.lock`
-----------

The current version is a good teaching baseline but has the two classic bugs to fix and document:

- Use `os.open(path, O_CREAT | O_EXCL)` for real atomicity.
- Write PID, hostname and timestamp into the file, so a stale lock is diagnosable.

Then add `timeout=` (block and retry instead of failing immediately) and stale-lock detection.

`just.args`
-----------

The richest place to extend, since each parser is about ten lines:

- `EnumArg` — maps a string to an `enum` member, listing the valid names in the error.
- `RangeArg` / `PositiveIntArg`
- `RegexArg` — returns a compiled pattern.
- `FileArg` — `argparse.FileType` leaks file handles on parse errors; worth documenting *why*
  it is being replaced.
- `BoolArg`
- `TimeDeltaArg` / `ByteSizeArg`, on top of `just.human`.

Also: `logging.getLevelNamesMapping()` (3.11+) is the public answer to the `logging._nameToLevel`
FIXME at [args.py:90](src/just/args.py#L90), with the private dict as a fallback.

`just.heap2`
------------

The docstring at [heap2.py:68](src/just/heap2.py#L68) already names the flaw: on key ties, `heapq`
falls through to comparing the items themselves. Fix it with the `itertools.count()` tie-breaker
from the `heapq` docs, which also makes `KeyHeap` stable and drops the `SupportsLessThan` bound on `T`.

Then add:

- `__bool__`, `__repr__`, `__iter__` (drain)
- `nsmallest` / `nlargest`
- `clear()`
- `PriorityQueue` with `update` / `remove`, via the lazy-deletion recipe — this one is the
  actual missing piece in the standard library.

Once `heap2` is complete, decorate [just.heap](src/just/heap.py) with `@deprecated`: dogfooding the
deprecation module during a real migration is a better demo than any test.

Other New Modules
=================

module          | fills                                                              | demonstrates
----------------|--------------------------------------------------------------------|----------------------------------------
`just.signals`  | graceful SIGINT/SIGTERM shutdown flag for long loops                | `signal`, restoring prior handlers on exit
`just.env`      | `env_bool`/`env_int`/`env_path` with defaults and validation, plus a `patch_env()` context-manager for tests | parse-don't-validate, test seams
`just.dicts`    | `deep_update`, `flatten`/`unflatten`, `get_path("a.b.c")`, `invert` | recursion over nested structures
`just.table`    | align a list of dicts into a text table                             | width computation, `str.format` specs
`just.progress` | dependency-free progress-bar that no-ops when not a tty             | `shutil.get_terminal_size`, `\r`, tty detection
`just.hash`     | chunked file checksums (`hashlib.file_digest` is 3.11+)             | buffered reads, `memoryview`
`just.cache`    | TTL cache decorator — `functools.lru_cache` has no expiry           | closures over mutable state, cache keys
`just.version`  | compare `1.2.3` version strings without `packaging`                 | `NamedTuple` plus `@total_ordering`
`just.subproc`  | run a command with timeout, capture, logging, rich error            | `subprocess` without `shell=True`

Project-Level Notes
===================

Doctests
--------

The docstrings contain `>>>` examples that nothing executes, and at least one is wrong:
[first.py:24-26](src/just/first.py#L24-L26) shows `>>> first_next([0, 0, 0])` printing `None`,
but a REPL prints nothing for `None`.

Adding `--doctest-modules` to the pytest run would make every `ex::` block a real test — high value
for a repo whose purpose is being copied from later.

Project Structure
=================

Defects
-------

These are bugs rather than nice-to-haves, and each is small.

**`src/just/py.typed` does not exist.** [setup.py:39](setup.py#L39) declares
`package_data={"just": ["py.typed"]}`, but there is no such file in [src/just/](src/just/).
Without that PEP 561 marker, every downstream `mypy` silently ignores all the annotations —
the type hints are decorative outside this repo. Fixed by adding one empty file.

**No `python_requires=`.** [setup.py](setup.py) carries classifiers for 3.6 through 3.13 but no
`python_requires`, so `pip` will install on any interpreter and the failure surfaces at import time.

**The version floor is stale, and the 3.7 CI job cannot be passing.** A `vermin` run reports:

    src/just/heap2.py   !2, 3.8      (typing.Protocol)
    src/just/args.py    !2, 3.13     (re.PatternError — false positive)

`heap2` needs **3.8+**, but the classifiers claim 3.6/3.7, [pyproject.toml:4](pyproject.toml#L4)
sets `target-version = ["py36"]`, and [tests.yml:28](.github/workflows/tests.yml#L28) still runs a
`"3.7"` matrix entry, which imports `heap2` and cannot. Separately, the `re.PatternError` hit at
[args.py:17](src/just/args.py#L17) is guarded by `try` / `except AttributeError`; `vermin` cannot see
the guard, so it needs a `# novermin` comment or the reported floor stays wrong at 3.13.

Optional Extras
---------------

[setup.py:43-49](setup.py#L43-L49) currently has `dev` (a grab-bag of four unrelated tools), `docs`,
and a `types` extra holding only `types-setuptools` while `mypy` itself sits in `dev`. Since testing
and documentation are already framed as separable features, the extras should match:

extra    | contents
---------|--------------------------------------------------
`test`   | `pytest`, `pytest-cov`
`lint`   | `black<26`, `flake8`, `vermin`
`types`  | `mypy`, `types-setuptools`
`docs`   | unchanged
`dev`    | `just-utils[test,lint,types,docs]` — recursive extras work fine in `pip`

That yields one extra per CI job, so `pip install -e .[types]` and the `mypy` step install exactly
the same thing.

Tool Configuration
------------------

- **No pytest configuration at all** — neither `[tool:pytest]` in [setup.cfg](setup.cfg) nor
  `[tool.pytest.ini_options]` in [pyproject.toml](pyproject.toml). Add `testpaths`, `-ra`,
  `--strict-markers`, and `--doctest-modules` (that last one is what turns the `ex::` blocks into
  real tests, per the Doctests note above).
- **No mypy configuration**, despite `mypy` being a dependency with its own script and a
  `.mypy_cache/` in the tree. A `[mypy]` section with `strict = True` plus per-module relaxations is
  itself a good reference artifact.
- **No `fail_under`** in `[coverage:report]`. The coverage badge is published, but nothing fails
  when coverage drops.
- **No `[build-system]` table** in [pyproject.toml](pyproject.toml), so builds go through the legacy
  setuptools fallback path. Three lines fixes it, and it is the modern-packaging demonstration this
  repo ought to carry.

Also worth adding to [setup.py](setup.py): `license="MIT"`, a `long_description` read from
[README.md](README.md) with `long_description_content_type="text/markdown"` (it is a hardcoded
one-liner today), and `project_urls`.

Continuous Integration
----------------------

- **`mypy` and `vermin` never run in CI**, though both are in `[dev]` and have scripts. Two steps
  closes the loop — and `vermin` in CI is what would have caught the 3.8 floor above.
- **The flake8 step cannot fail.** [tests.yml:56-61](.github/workflows/tests.yml#L56-L61) is the
  unmodified GitHub template: the second invocation passes `--exit-zero`, and its
  `--max-line-length=127` contradicts the 120 in [setup.cfg:16](setup.cfg#L16). Replacing both lines
  with a plain `flake8 src/ tests/ setup.py` picks up setup.cfg instead.
- **`on: [push]` only** — no `pull_request` trigger.
- **Add `windows-latest` and `macos-latest` to the matrix.** Justified here rather than
  cargo-culted: `just.lock` does exclusive file creation and unlinking, `just.open` handles paths,
  and the planned `just.atomic` (`os.replace`) and `just.signals` (SIGTERM) are precisely where
  POSIX assumptions break on Windows — the development platform.
- **The coverage-badge steps run once per matrix entry.** Guard them with
  `if: matrix.python-version == '3.14' && matrix.os == 'ubuntu-latest'`.
- **Drift between the two workflows**: tests.yml uses `checkout@v3` / `setup-python@v4`, docs.yml
  uses v4 / v5. Also missing from tests.yml: `cache: pip` on setup-python, a `concurrency:` group to
  cancel superseded runs, and a `permissions:` block (docs.yml has one).

Repository Files
----------------

- **`CHANGELOG.md`** — thematically required by
  [`@deprecated(since=...)`](src/just/deprecate.py#L12): the `since` string has to point somewhere.
- **`__version__` in [src/just/\_\_init\_\_.py](src/just/__init__.py)** (currently empty),
  single-sourced into setup.py. The version lives only in setup.py today, so it is unavailable at
  run-time.
- **Decide on the generated docs.** `docs/just.rst` and `docs/modules.rst` are committed,
  `run_docs_build.sh` regenerates them, `run_docs_clean.sh` deletes them, and `docs.yml` never runs
  `sphinx-apidoc` — so the deployed docs only pick up a new module if the regenerated `.rst` gets
  committed. Either gitignore them and run `sphinx-apidoc` in the workflow, or stop regenerating them
  locally. Also add `-W` to fail the docs build on warnings; it would surface the `_static` warning
  already noted in docs.yml.
- `.venv/` is listed under the `# vscode` comment in [.gitignore](.gitignore).
- `just-utils/` at the repo root is an empty leftover directory.

Scripts
-------

- **`pushd` / `popd` under `#!/bin/sh` is a bashism** in `run_docs_build.sh`, `run_docs_clean.sh`
  and `run_docs_server.sh` — they break under `dash`, which is `/bin/sh` on the Ubuntu CI runner.
  Use `cd` in a subshell, or switch the shebang to `#!/bin/bash`.
- `run_docs_build.sh` invokes `./make.bat` from a POSIX script — Windows-only, and it is the one
  script CI would most want to reuse.
- **One entry point.** A `Makefile` (or `run_all.sh`) with `format lint types test docs coverage all`
  targets, which CI then calls, is the standard fix for scripts and CI drifting apart — exactly what
  happened with the flake8 line-length above. `tox` or `nox` would do it properly across the version
  matrix, at the cost of a dev-only external dependency.
- `run_black.sh` only has `--check`, so the most-used tool has no format-in-place script.

Suggested Order
===============

0. The three defects above: `py.typed`, `python_requires`, and the 3.8 version floor
   (classifiers, black `target-version`, CI matrix, `# novermin` on [args.py:17](src/just/args.py#L17)).
1. `just.human` — unblocks the `just.timing` and `just.args` extensions.
2. `just.retry`
3. `just.timing` fixes (the `@timed()` FIXME, `ContextDecorator`, `try/finally`).
4. `just.atomic`
5. `just.log`, then the `just.args` additions.
6. `just.heap2` completion, then deprecate `just.heap`.
7. Everything else, as needed.

Structural work is independent of the module work and can interleave; the extras split and the
pytest configuration are worth doing early, since `--doctest-modules` and a `test` extra change how
every new module gets tested.
