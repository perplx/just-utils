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

`just.atomic`
-------------

`with atomic_open(path, mode) as f:` — writes to a temporary file in the same directory and
`os.replace()`s it into place on clean exit, discarding it on exception.

A genuine standard-library gap, and a *correctness* lesson: same-filesystem temp file,
`os.replace` atomicity, `fsync` before rename, cleanup in `finally`.
Conceptually the sibling of [just.lock](src/just/lock.py).

[atomic.py](src/just/atomic.py) currently holds a sketch that does not work, and every bug in
it is one of the lessons:

- `TemporaryFile` has no usable `.name` and deletes itself on close, so the
  `os.replace(temp_file.name, ...)` at [atomic.py:18](src/just/atomic.py#L18) runs after the
  file is already gone — it must be `NamedTemporaryFile(..., delete=False)`.
- `yield from temp_file` at [atomic.py:16](src/just/atomic.py#L16) iterates the file's lines
  instead of handing the handle to the caller; it should be `yield temp_file`.
- No `fsync` before the rename, no `try` / `except` to unlink the temp file when the body
  raises, and no rejection of non-writing modes (the temp file starts empty, so `"a"` and
  `"r"` are lies).
- `main()` calls `atomic_open.write(...)` on the function object, so the demo cannot run.
- Module docstring is `"""FIXME"""`, and there is no `tests/test_atomic.py` — the only module
  in the package without a test file.

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

Finishing Touches
=================

These modules exist and pass, but are not finished. Each entry lists only what is left.

`just.retry`
------------

Working `retry()` decorator plus the `RetryIterator` / `RetryContext` form. Remaining, from
the module's own FIXMEs:

- `backoff=` and `jitter=` parameters — the jitter is half the point of the module,
  and *why* it matters is the lesson worth writing down.
- A `logger=` parameter, matching the rest of the package.
- Accept a tuple of exception types: `Union[Type[Exception], Tuple[Type[Exception], ...]]`.
- Decide whether [`RetryContext.__exit__`](src/just/retry.py#L56) should keep swallowing the
  exception unconditionally, and document whichever way it goes.

`just.human`
------------

`format_bytes` / `parse_bytes` / `format_duration` / `parse_duration` all work and have tests.
Remaining:

- The module docstring is still `"""FIXME"""`, and no function has an `ex::` block.
- `main()` has a stray `raise SystemExit` at [human.py:113](src/just/human.py#L113) that makes
  half the demo dead code.
- `parse_bytes` is annotated `-> int` but returns a float.
- Decide between ls-style units (`1.0K`, what is implemented) and IEC (`10.5 MiB`, what this
  plan originally specified), and record the choice rather than leaving both names in the file.
- The round-trip property test (`parse(format(x)) == x`) this module was chosen to demonstrate.
- Wire it into its two consumers: `just.timing` should print `1m 03s` instead of
  `63.000 seconds`, and `just.args` gets `DurationArg` / `ByteSizeArg` for free.

Extensions to Existing Modules
==============================

`just.timing`
-------------

Three things:

1. Kill the `@timed` vs `@timed()` FIXME at [timing.py:16](src/just/timing.py#L16) using the
   `callable(arg)` trick already written in [deprecate.py:86](src/just/deprecate.py#L86).
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

- `RangeArg` / `PositiveIntArg`
- `RegexArg` — returns a compiled pattern.
- `FileArg` — `argparse.FileType` leaks file handles on parse errors; worth documenting *why*
  it is being replaced.
- `BoolArg`
- `DurationArg` / `ByteSizeArg`, on top of `just.human`.

`EnumArg` exists and is tested, but still needs its `"""FIXME"""` docstring at
[args.py:93](src/just/args.py#L93) written with an `ex::` block like its neighbours, and a
decision on the case-insensitivity FIXME at [args.py:100](src/just/args.py#L100).

Also: `logging.getLevelNamesMapping()` (3.11+) is the public answer to the `logging._nameToLevel`
FIXME at [args.py:105](src/just/args.py#L105), used at
[args.py:131](src/just/args.py#L131), with the private dict as a fallback.

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

Project Structure
=================

Defects
-------

These are bugs rather than nice-to-haves, and each is small.

**The version floor is wrong by four minor versions, and the 3.7 CI job cannot be passing.**
The declared floor is 3.6, but four separate features push the real one to **3.10**:

    src/just/retry.py   3.10   typing.ParamSpec
    src/just/atomic.py  3.10   PEP 604 unions in annotations (Path | str)
    src/just/human.py   3.9    builtin generics (tuple[float, int])
    src/just/heap2.py   3.9    builtin generics (list[tuple[K, T]])
    src/just/heap2.py   3.8    typing.Protocol
    src/just/args.py    3.13   re.PatternError — false positive, see below

Every declaration of the floor disagrees with that: [setup.py:41](setup.py#L41) says
`python_requires=">=3.6"`, the classifiers at [setup.py:26-33](setup.py#L26-L33) advertise 3.6
through 3.13 (the first four of which are false), [pyproject.toml:4](pyproject.toml#L4) sets
`target-version = ["py36"]`, and
[tests.yml:28](.github/workflows/tests.yml#L28) still runs a `"3.7"` matrix entry that cannot
import half the package. Fixing it means editing all four in one go.

Separately, the `re.PatternError` hit at [args.py:19](src/just/args.py#L19) is guarded by
`try` / `except AttributeError`; `vermin` cannot see the guard, so it needs a `# novermin` comment
or the reported floor stays wrong at 3.13.

Tool Configuration
------------------

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
  closes the loop — and `vermin` in CI is what would have caught the 3.10 floor above,
  which drifted twice without anyone noticing.
- **The flake8 step cannot fail.** [tests.yml:56-61](.github/workflows/tests.yml#L56-L61) is the
  unmodified GitHub template: the second invocation passes `--exit-zero`, and its
  `--max-line-length=127` contradicts the 120 in [setup.cfg:16](setup.cfg#L16). Replacing both lines
  with a plain `flake8 src/ tests/ setup.py` picks up setup.cfg instead.
- **`on: [push]` only** — no `pull_request` trigger.
- **Add `windows-latest` and `macos-latest` to the matrix.** Justified here rather than
  cargo-culted: `just.lock` does exclusive file creation and unlinking, `just.open` handles paths,
  and `just.atomic` (`os.replace`, `NamedTemporaryFile(delete=False)`) is precisely where POSIX
  assumptions break on Windows — which is the development platform, and is *shipped but never
  tested on any OS by CI*. The planned `just.signals` (SIGTERM) will be the same story.
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

0. The version floor: `python_requires`, classifiers, black `target-version`, CI matrix,
   and `# novermin` on [args.py:19](src/just/args.py#L19).
1. `just.atomic` — the module is currently a non-working sketch, so it is the one place the repo
   ships something wrong. Plus `tests/test_atomic.py`.
2. The `just.human` polish, then `just.timing` (the `@timed()` FIXME, `ContextDecorator`,
   `try/finally`) as its first consumer.
3. `just.log`, then the remaining `just.args` parsers.
4. `just.retry` finishing touches (backoff, jitter, `logger=`).
5. `just.heap2` completion, then deprecate `just.heap`.
6. Everything else, as needed.

Structural work is independent of the module work and can interleave.

Already Done
============

Removed from the plan as completed; kept here so the history stays legible.

- `just.human`, `just.retry` (core), `just.first` (`last` / `only` on a `_MISSING` sentinel),
  and `args.EnumArg` — see **Finishing Touches** above for what is still outstanding on the
  first two, and `just.args` for `EnumArg`.
- `src/just/py.typed`, `python_requires=` (present, though the value is wrong — see **Defects**),
  and the `test` / `lint` / `types` / `docs` / `dev` extras split in
  [setup.py](setup.py), which now gives one extra per CI job.
- `[tool.pytest.ini_options]` in [pyproject.toml](pyproject.toml): `testpaths`, `-ra`,
  `--strict-markers`, `--doctest-modules`.
- Doctests, via that `--doctest-modules`, with `src` in `testpaths` so the flag actually reaches
  the package. Two things worth remembering: the `unittest` `load_tests` protocol is **not
  supported by pytest**, so the hand-rolled doctest hooks it replaced had never run; and examples
  asserting on wall-clock timings need an inline `# doctest: +ELLIPSIS` directive rather than a
  transcribed number.
- Still outstanding from that last one: the `ex::` blocks in `args.py`, `atomic.py` and `lock.py`
  are plain indented code without `>>>` prompts, so nothing executes them. Converting the ones that
  touch the filesystem would need `tmp_path`-style scaffolding.
