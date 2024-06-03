# mpacklog.py

[![Build](https://img.shields.io/github/actions/workflow/status/upkie/mpacklog.py/ci.yml?branch=main)](https://github.com/upkie/mpacklog.py/actions)
[![Documentation](https://img.shields.io/github/actions/workflow/status/upkie/mpacklog.py/docs.yml?branch=main&label=docs)](https://upkie.github.io/mpacklog.py/)
[![Coverage](https://coveralls.io/repos/github/upkie/mpacklog.py/badge.svg?branch=main)](https://coveralls.io/github/upkie/mpacklog.py?branch=main)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/mpacklog.svg)](https://anaconda.org/conda-forge/mpacklog)
[![PyPI version](https://img.shields.io/pypi/v/mpacklog)](https://pypi.org/project/mpacklog/)

Stream dictionaries to files or over the network using MessagePack in Python.

## Installation

### From conda-forge

```console
conda install -c conda-forge mpacklog
```

### From PyPI

```console
pip install mpacklog
```

## Usage

#### Asynchronous API

Add messages to the log using the [`put`](https://scaron.info/doc/mpacklog/classmpacklog_1_1mpacklog_1_1python_1_1logger_1_1Logger.html#aa0f928ac07280acd132627d8545a7e18) function, have them written to file in the separate [`write`](https://scaron.info/doc/mpacklog/classmpacklog_1_1mpacklog_1_1python_1_1logger_1_1Logger.html#acbea9c05c465423efc3f38a25ed699d2) coroutine.

```python
import asyncio
import mpacklog

async def main():
    logger = mpacklog.AsyncLogger("output.mpack")
    await asyncio.gather(main_loop(logger), logger.write())

async def main_loop(logger):
    for bar in range(1000):
        await asyncio.sleep(1e-3)
        await logger.put({"foo": bar, "something": "else"})
    await logger.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

#### Synchronous API

The synchronous API is similar to the asynchronous API, except it doesn't provide a ``stop`` method and the ``put`` and ``write`` methods are blocking.

```python
import mpacklog

logger = mpacklog.SyncLogger("output.mpack")

for bar in range(1000):
    logger.put({"foo": bar, "something": "else"})

# Flush all messages to the file
logger.write()
```

## Command-line

The ``mpacklog`` utility provides commands to manipulate ``.mpack`` files.

### ``dump``

The ``dump`` command writes down a log file to [newline-delimited JSON](https://jsonlines.org):

```console
mpacklog dump my_log.mpack
```

### ``list``

This commands lists all nested dictionary keys encountered in a log file. Nested keys are separated by slashes ``/`` in the output. For instance, if some dictionaries in ``my_log.mpack`` contain values at ``dict["foo"]["bar"]`` and ``dict["foo"]["cbs"]``, the command will produce:

```
$ mpacklog list my_log.mpack
- foo/bar
- foo/cbs
```

### ``serve``

The ``serve`` command watches a log file for updates and serves the last dictionary appended to it over the network. Its argument is either a log file or a directory containing log files. In the second case, the most recent log files in the directory is opened:

```
$ mpacklog serve /var/log/my_mpack_logs/
```

You can use [`mpackview`](https://pypi.org/project/mpackview) to connect a live plot to the server, or develop your own tool (the server API is quite simple).

## See also

* [foxplot](https://github.com/stephane-caron/foxplot): explore and plot time-series data from MessagePack and line-delimited JSON files.
* [jq](https://github.com/stedolan/jq): manipulate JSON series to add, remove or extend fields.
* [mpacklog.cpp](https://github.com/upkie/mpacklog.cpp): log dictionaries to MessagePack files in C++.
* [rq](https://github.com/dflemstr/rq): transform from/to MessagePack, JSON, YAML, TOML, etc. For instance ``mpacklog dump`` is equivalent to ``rq -mJ < my_log.mpack``.
