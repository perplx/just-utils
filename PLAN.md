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

It is also already wired into [docs/just.rst](docs/just.rst), so the published API docs
advertise the broken module.

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
- Decide whether [`RetryContext.__exit__`](src/just/retry.py#L73) should keep swallowing the
  exception unconditionally (the `return True` FIXME at [retry.py:78](src/just/retry.py#L78)),
  and document whichever way it goes. The consequence of today's choice: when every attempt
  fails, `RetryIterator` simply runs out, and the caller never sees the last exception.

`just.human`
------------

`format_bytes` / `parse_bytes` / `format_duration` / `parse_duration` all work and have tests;
the module has a real docstring, and `format_bytes` has an `ex::` block. Remaining:

- `parse_bytes`, `format_duration` and `parse_duration` have no `ex::` block.
- `main()` has a stray `raise SystemExit` at [human.py:152](src/just/human.py#L152) that makes
  half the demo dead code.
- `parse_bytes` is annotated `-> int` but returns a float.
- The `ValueError` messages at [human.py:26](src/just/human.py#L26) and
  [human.py:55](src/just/human.py#L55) are missing their `f` prefix, so they print a literal
  `{num_bytes}`; and the check is duplicated, since `format_bytes` calls `_find_blocks`.
- `format_bytes(1024**2 - 1)` returns `'1024K'` instead of rolling over to `1.0M`, and
  [test_human.py:22](tests/test_human.py#L22) pins the bug with a FIXME rather than failing on it.
- `format_duration` of a float yields `1.0m 3.5s`, which `parse_duration` (ints only) cannot
  read back — the round-trip breaks for anything that is not a whole number of seconds.
- Decide between ls-style units (`1.0K`, what is implemented) and IEC (`10.5 MiB`, what this
  plan originally specified), and record the choice rather than leaving both `IEC_UNITS` and
  `LS_UNITS` in the file.
- The round-trip property test (`parse(format(x)) == x`) this module was chosen to demonstrate.
- `tests/test_human.py` still has a `"""FIXME"""` module docstring.
- Wire it into its two consumers: `just.timing` should print `1m 03s` instead of
  `63.000 seconds`, and `just.args` gets `DurationArg` / `ByteSizeArg` for free.

`just.cache`
------------

`memoize` and `ttl_cache` work, have tests, and are in the README. Remaining:

- `ttl_cache` measures expiry with `time.time()`, which jumps when the wall clock is adjusted;
  `time.monotonic()` is the right clock for intervals, and that distinction is the lesson.
- Expired entries are only replaced, never evicted, so the cache grows without bound. Add a
  `maxsize=` and a `cache_clear()`, as `functools.lru_cache` has.
- `ttl_cache` has no return annotation, and neither function has `:param:` docs.
- [test_cache.py](tests/test_cache.py) waits on a real `time.sleep(1)` loop; an injectable
  clock would make it instant and deterministic.

`just.first`
------------

- `only()` has no docstring or `ex::` block, unlike `first` and `last` beside it.
- `default=` is untyped, and `-> Optional[T]` hides that the no-default form never returns
  `None`. An `@overload` pair is the precise fix.

Extensions to Existing Modules
==============================

`just.timing`
-------------

Three things:

1. Kill the `@timed` vs `@timed()` FIXME at [timing.py:15](src/just/timing.py#L15) (and its twin at
   [test_timing.py:22](tests/test_timing.py#L22)) using the `callable(arg)` trick already written in
   [deprecate.py:88](src/just/deprecate.py#L88). Same problem, same solution, two modules apart —
   worth unifying.
2. Replace both the decorator and the context-manager with one `Timer(contextlib.ContextDecorator)`
   class that works as `with Timer(...)` *and* `@Timer(...)`, and exposes `.elapsed` afterwards so
   callers can assert on the number instead of scraping stdout. `ContextDecorator` is an underused
   standard-library gem and this is the textbook case for it.
3. The context-manager doesn't record the time if the body raises — the `yield` at
   [timing.py:93](src/just/timing.py#L93) should be in a `try/finally`, the way `lock_file` already
   does it.

`just.open`
-----------

- Add `.lzma` (same `lzma.open` as `.xz`) and `.zip`.
- Replace the `if`-chain with an extension-to-opener registry dict, so adding a format is one line.
  With three branches now, the chain is already the thing that grows.
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

Also: `logging.getLevelNamesMapping()` (3.11+) is the public answer to the `logging._nameToLevel`
FIXME at [args.py:124](src/just/args.py#L124), used at
[args.py:152-154](src/just/args.py#L152-L154), with the private dict as a fallback.

[test_args.py](tests/test_args.py) carries four FIXMEs about `os.chmod` not removing access on
Windows — concrete evidence for the Windows CI job below.

`just.heap2`
------------

The docstring at [heap2.py:112](src/just/heap2.py#L112) already names the flaw: on key ties, `heapq`
falls through to comparing the items themselves. Fix it with the `itertools.count()` tie-breaker
from the `heapq` docs, which also makes `KeyHeap` stable and drops the `SupportsLessThan` bound on `T`.

That changes the stored tuples to `(key, count, item)`, so rework `KeyHeap.__repr__` in the same
change: today it prints the internal tuples and the raw key function
(`KeyHeap([(1, 'c'), ...], key=<built-in function len>)`), which reads like a constructor call but
is not one, and a lambda key puts a memory address in it. Either make it a valid call
(`KeyHeap(['c', 'bb', 'aaa'], key=len)`, using the key's `__qualname__`) or use the
`<KeyHeap ...>` form that signals it cannot be evaluated; `test_repr` pins the current output.

The `Heap` class still has a `"""FIXME"""` docstring ([heap2.py:26](src/just/heap2.py#L26)).
`main()` could demo `drain()` instead of its `while len(heap) > 0` loop.

Then add:

- `nsmallest` / `nlargest`
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
`just.version`  | compare `1.2.3` version strings without `packaging`                 | `NamedTuple` plus `@total_ordering`
`just.subproc`  | run a command with timeout, capture, logging, rich error            | `subprocess` without `shell=True`

Project Structure
=================

Defects
-------

These are bugs rather than nice-to-haves, and each is small.

**The declared version floor is 3.6, the real one is 3.10, and CI tests neither.**
Five separate features push the real floor to **3.10**:

    src/just/retry.py      3.10   typing.ParamSpec
    src/just/cache.py      3.10   typing.ParamSpec
    src/just/deprecate.py  3.10   typing.ParamSpec, PEP 604 union in a signature (str | None)
    src/just/atomic.py     3.10   PEP 604 unions in annotations (Path | str)
    src/just/human.py      3.9    builtin generics (tuple[float, int])
    src/just/heap2.py      3.9    builtin generics (list[tuple[K, T]])
    src/just/heap2.py      3.8    typing.Protocol
    src/just/args.py       3.13   re.PatternError — false positive, see below

Every declaration of the floor disagrees with that: [setup.py:41](setup.py#L41) says
`python_requires=">=3.6"`, the classifiers at [setup.py:26-33](setup.py#L26-L33) advertise 3.6
through 3.13 (the first four of which are false), and [pyproject.toml:4](pyproject.toml#L4) sets
`target-version = ["py36"]`. Meanwhile the CI matrix at
[tests.yml:29](.github/workflows/tests.yml#L29) is `["3.11", "3.14"]`, so the real floor is never
tested either. Fixing it means editing all four in one go, with the matrix becoming `["3.10", "3.14"]`.

Separately, the `re.PatternError` hit at [args.py:17](src/just/args.py#L17) is guarded by
`try` / `except AttributeError`; `vermin` cannot see the guard, so it needs a `# novermin` comment
or the reported floor stays wrong at 3.13. The same two lines are also the only mypy error in
`args.py` ([args.py:19](src/just/args.py#L19): "Cannot assign multiple types to name
`PatternError`"); annotating the first assignment as `PatternError: Type[Exception]` fixes it.

**The pytest configuration depends on an unpinned pytest.** [pyproject.toml:6](pyproject.toml#L6)
uses the native `[tool.pytest]` table, which only pytest 9+ reads, but the `test` extra is just
`pytest-cov`. On an older pytest the table is silently ignored, `--doctest-modules` and `src/` drop
out, and the doctests quietly stop running. Either pin `pytest>=9` or use `[tool.pytest.ini_options]`.

**`download_url`** at [setup.py:19](setup.py#L19) points at `refs/heads/master`; the branch is `main`.

**Short title underlines** in [docs/just.rst](docs/just.rst) for `just.atomic`, `just.cache` and
`just.retry` are Sphinx warnings today, and will be errors once `-W` (below) is on.

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
- **`-ra` and `--strict-markers`** are not in the pytest `addopts` yet.

Also worth adding to [setup.py](setup.py): `license="MIT"`, a `long_description` read from
[README.md](README.md) with `long_description_content_type="text/markdown"` (it is a hardcoded
one-liner today), `project_urls`, and a real `author_email` (currently `""`).

Continuous Integration
----------------------

- **`mypy` and `vermin` never run in CI**, though both are in `[dev]` and have scripts. Two steps
  closes the loop — and `vermin` in CI is what would have caught the 3.10 floor above,
  which drifted twice without anyone noticing.
- **`on: [push]` only** — no `pull_request` trigger.
- **Add `windows-latest` and `macos-latest` to the matrix.** Justified here rather than
  cargo-culted: `just.lock` does exclusive file creation and unlinking, `just.open` handles paths,
  and `just.atomic` (`os.replace`, `NamedTemporaryFile(delete=False)`) is precisely where POSIX
  assumptions break on Windows — which is the development platform, and is *shipped but never
  tested on any OS by CI*. The planned `just.signals` (SIGTERM) will be the same story.
- **The coverage-badge steps run once per matrix entry.** Guard them with
  `if: matrix.python-version == '3.14'` (adding `&& matrix.os == 'ubuntu-latest'` once the OS
  matrix exists).
- **Missing from tests.yml**: a `concurrency:` group to cancel superseded runs, and a
  `permissions:` block (docs.yml has one).
- **Leftover template scaffolding in tests.yml**: the "Install dependencies" step only upgrades pip
  around commented-out lines, and five FIXME comments remain. Fold it into the `pip install -e .[dev]`
  step and clear the FIXMEs as their items land.

Repository Files
----------------

- **`CHANGELOG.md`** — thematically required by
  [`@deprecated(since=...)`](src/just/deprecate.py#L14): the `since` string has to point somewhere.
- **`__version__` in [src/just/\_\_init\_\_.py](src/just/__init__.py)** (currently empty),
  single-sourced into setup.py. The version lives only in setup.py today, so it is unavailable at
  run-time.
- **Decide on the generated docs.** `docs/just.rst` and `docs/modules.rst` are committed,
  `run_docs_build.sh` regenerates them, `run_docs_clean.sh` deletes them, and `docs.yml` never runs
  `sphinx-apidoc` — so the deployed docs only pick up a new module if the regenerated `.rst` gets
  committed. Either gitignore them and run `sphinx-apidoc` in the workflow, or stop regenerating them
  locally. Also add `-W` to fail the docs build on warnings; it would surface the `_static` warning
  already noted in docs.yml.
- **README drift**: the feature list omits `just.retry` and `just.atomic`, describes `just.first`
  without `last` / `only`, the "Config Files" table says pyproject.toml configures only black (it
  also configures pytest), and there are typos ("imprements", "redisign", "betwees", "interable").
- `.venv/` is listed under the `# vscode` comment in [.gitignore](.gitignore).
- `just-utils/` at the repo root is an empty leftover directory — local only, since git does not
  track empty directories.

Scripts
-------

- **`pushd` / `popd` under `#!/bin/sh` is a bashism** in `run_docs_build.sh`, `run_docs_clean.sh`
  and `run_docs_server.sh` — they break under `dash`, which is `/bin/sh` on the Ubuntu CI runner.
  Use `cd` in a subshell, or switch the shebang to `#!/bin/bash`.
- `run_docs_build.sh` invokes `./make.bat` from a POSIX script — Windows-only, and it is the one
  script CI would most want to reuse.
- **One entry point.** A `Makefile` (or `run_all.sh`) with `format lint types test docs coverage all`
  targets, which CI then calls, is the standard fix for scripts and CI drifting apart — exactly what
  happened with the flake8 line-length. `tox` or `nox` would do it properly across the version
  matrix, at the cost of a dev-only external dependency.
- `run_black.sh` only has `--check`, so the most-used tool has no format-in-place script.
- `run_doctest.sh` duplicates `--doctest-modules`, but through `python -m doctest`, so the two can
  disagree; `run_flake8.sh` lists `setup.py` twice; `run_coverage.sh` sets `$verbose` and never
  uses it.

Suggested Order
===============

0. The version floor: `python_requires`, classifiers, black `target-version`, CI matrix to
   `["3.10", "3.14"]`, and `# novermin` on [args.py:17](src/just/args.py#L17).
1. `just.atomic` — the module is currently a non-working sketch, so it is the one place the repo
   ships something wrong. Plus `tests/test_atomic.py`.
2. The `just.human` polish (including the f-string, `1024K` and float round-trip bugs), then
   `just.timing` (the `@timed()` FIXME, `ContextDecorator`, `try/finally`) as its first consumer.
3. `just.log`, then the remaining `just.args` parsers.
4. `just.retry` finishing touches (backoff, jitter, `logger=`).
5. `just.cache` finishing touches (`monotonic`, eviction) — small and self-contained.
6. `just.heap2` completion, then deprecate `just.heap`.
7. Everything else, as needed.

Structural work is independent of the module work and can interleave.

Already Done
============

Removed from the plan as completed; kept here so the history stays legible.

- `just.human`, `just.retry` (core), `just.first` (`last` / `only` on a `_MISSING` sentinel),
  `just.cache` (`memoize` / `ttl_cache`, with tests and a README entry), and `args.EnumArg` with
  its docstring and doctest — see **Finishing Touches** above for what is still outstanding.
- `EnumArg` return type: it is now `Generic[E]` with `E = TypeVar("E", bound=Enum)`, takes
  `Type[E]`, and looks members up with `enum_type[name]`, so mypy infers `EnumArg(Color)("RED")` as
  `Color`. Two lessons from the fix: `getattr` returns `Any`, so it made the `-> E` annotation an
  unchecked promise, and it also accepted any class attribute (`mro`, `__class__`) as a value.
  `[]` only ever looks in the member map, so that bug is ruled out by construction rather than
  guarded by a test.
  `[]` raises `KeyError`, which argparse does not catch, so it has to become
  `ArgumentTypeError`. The tests' `TestEnum` was a plain class rather than an `Enum`, which
  `getattr` had hidden; it is a real `enum.Enum` now. Decided: names match case-sensitively,
  exactly as declared — upper-casing the input would break enums whose member names are not
  upper-case.
- `.xz` support in `just.open`, with test data and a doctest for every format.
- `src/just/py.typed`, `python_requires=` (present, though the value is wrong — see **Defects**),
  and the `test` / `lint` / `types` / `docs` / `dev` extras split in
  [setup.py](setup.py), which now gives one extra per CI job.
- pytest configuration in [pyproject.toml](pyproject.toml): `testpaths` and `--doctest-modules`
  (in a `[tool.pytest]` table — see **Defects** for the version caveat).
- Doctests, via that `--doctest-modules`, with `src` in `testpaths` so the flag actually reaches
  the package. Two things worth remembering: the `unittest` `load_tests` protocol is **not
  supported by pytest**, so the hand-rolled doctest hooks it replaced had never run; and examples
  asserting on wall-clock timings need an inline `# doctest: +ELLIPSIS` directive rather than a
  transcribed number.
- Every `ex::` block in `args.py` is now a real `>>>` doctest, and `first` / `last` / `format_bytes`
  gained them too. Still outstanding: the blocks in `atomic.py` and `lock.py` are plain indented
  code, so nothing executes them (converting them would need `tmp_path`-style scaffolding), and
  `retry.py`'s are marked `+SKIP`.
- CI: the flake8 step was the unmodified GitHub template (`--exit-zero`, `--max-line-length=127`);
  it is now a plain `flake8 src/ tests/ setup.py` that reads setup.cfg. Actions are on
  `checkout@v4` / `setup-python@v5` with `cache: 'pip'`, matching docs.yml.
- `just.heap2`: `__repr__` on both classes (built from `type(self).__name__`, so subclasses print
  their own name), `drain()`, which pops every item in order, and `clear()`, which empties the
  list in place (safe, since `__init__` copies its input) and keeps `KeyHeap`'s key function; its
  tests push after clearing to prove the ordering still works. Two decisions worth keeping:
  - Draining is an explicit `drain()` method, not `__iter__`. Python iterates for far more than
    `for` loops: with a popping `__iter__` and no `__contains__`, `x in heap` popped items until it
    found `x`, and `list()`, `sorted()`, `print(*heap)` and debugger views all emptied the heap.
    The standard library's draining containers (`queue.Queue`, `asyncio.Queue`) define no
    `__iter__` for the same reason. Without one, `x in heap` now raises `TypeError` — a loud
    failure instead of silent data loss. A non-destructive `__iter__` (over `sorted(self._heap)`)
    plus a `__contains__` can be added later if wanted.
  - No `__bool__`: when a class defines none, `bool()` calls `__len__` and treats `0` as false.
    That is the data model's documented truth protocol, not a side effect, and it is what `list`
    and `deque` rely on; a separate `__bool__` would only be one more thing to keep in sync.
    `test_bool` still pins the behaviour.
