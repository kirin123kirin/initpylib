#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from glob import glob
from timeit import timeit

from tempfile import TemporaryDirectory
from os.path import dirname

tdir = dirname(__file__)

class _tmpdir(TemporaryDirectory):
    def __del__(self):
        self.cleanup()
_tmp = _tmpdir()
TMPDIR = _tmp.name

from psutil import Process
from datetime import datetime
if sys.version_info[:2] >= (3, 7):
    from datetime import timezone, timedelta
PY2 = sys.version_info[0] == 2

# github action problem in windows default codepage 1252 environment
# https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
defaultencoding = 'utf-8'
if sys.stdout.encoding != defaultencoding:
    if PY2:
        reload(sys)
        sys.setdefaultencoding(defaultencoding)
    elif os.name == "nt":
        sys.stdout.reconfigure(encoding=defaultencoding)

from os.path import dirname, abspath, join as pjoin
shome = abspath(pjoin(dirname(__file__), ".."))
sys.path.insert(0, pjoin(shome, "build"))
sys.path.insert(0, pjoin(shome, "build", "cmake-build"))
sys.path.insert(0, pjoin(shome, "_skbuild", "cmake-build"))
sys.path.insert(0, pjoin(shome, "build", "cmake-install"))
sys.path.insert(0, pjoin(shome, "_skbuild", "cmake-install"))
try:
    from _PLEASE_PYPROJECT_NAME_ import *
    kw = {"setup": "from _PLEASE_PYPROJECT_NAME_ import *"} if PY2 else {}
except ImportError:
    try:
        from __PLEASE_PYPROJECT_NAME_ import *
        kw = {"setup": "from __PLEASE_PYPROJECT_NAME_ import *"} if PY2 else {}
    except ImportError:
        from _PLEASE_PYPROJECT_NAME_.__PLEASE_PYPROJECT_NAME_ import *
        kw = {"setup": "from _PLEASE_PYPROJECT_NAME_.__PLEASE_PYPROJECT_NAME_ import *"} if PY2 else {}

process = Process(os.getpid())
def memusage():
    return process.memory_info()[0] / 1024

def runtimeit(funcstr, number=10000):
    i = 0
    kw["number"] = number
    if sys.version_info[0] >= 3:
        kw["globals"] = globals()

    for fc in funcstr.strip().splitlines():
        fc = fc.strip()

        if i == 0:
            timeit(fc, **kw)
        bm = memusage()
        p = timeit(fc, **kw)

        am = (memusage() - bm)
        assert am < 10000, "{} function {}KB Memory Leak Error".format(fc, am)
        print("{}: {} ns (mem after {}KB)".format(fc, int(1000000000 * p / number), am))
        i += 1


def test__PLEASE_PYPROJECT_NAME_():
    assert(_PLEASE_PYPROJECT_NAME_("hello"))


def test__PLEASE_PYPROJECT_NAME__perf():
    runtimeit('pass')


if __name__ == '__main__':
    import os
    import traceback

    curdir = os.getcwd()
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        for fn, func in dict(locals()).items():
            if fn.startswith("test_"):
                print("Runner: %s" % fn)
                func()
    except Exception as e:
        traceback.print_exc()
        raise (e)
    finally:
        os.chdir(curdir)
