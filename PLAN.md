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

Housekeeping
------------

- `just-utils/` at the repo root is an empty leftover directory.
- [setup.py](setup.py) classifies 3.6+, while `heap2` uses `Protocol` (3.8+) and `list[tuple[...]]`
  (3.9+). Worth a `vermin` run ([scripts/run_vermin.sh](scripts/run_vermin.sh)) to resync the claim.

Suggested Order
===============

1. `just.human` — unblocks the `just.timing` and `just.args` extensions.
2. `just.retry`
3. `just.timing` fixes (the `@timed()` FIXME, `ContextDecorator`, `try/finally`).
4. `just.atomic`
5. `just.log`, then the `just.args` additions.
6. `just.heap2` completion, then deprecate `just.heap`.
7. Everything else, as needed.
