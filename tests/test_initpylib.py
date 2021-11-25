#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from tempfile import TemporaryDirectory
try:
    from __main__ import main
except (ModuleNotFoundError, ImportError):
    from initpylib.__main__ import main

origargs = sys.argv.copy()

def _script_call_capi_ok_test(subcmd):
    sys.argv[:] = origargs
    tmpdir = TemporaryDirectory()
    sys.argv.extend([subcmd, tmpdir.name])
    main()
    tmp_n = sum(len(dirs) + len(files) for _, dirs, files in os.walk("templates_capi"))
    build_n = sum(len(dirs) + len(files) for _, dirs, files in os.walk(tmpdir.name))
    assert(build_n >= tmp_n)

def test_script_call_capi_ok_test():
    _script_call_capi_ok_test("capi")

def test_script_call_py_ok_test():
    _script_call_capi_ok_test("py")

def test_script_call_exception_test1():
    sys.argv[:] = origargs
    try:
        main()
    except SystemExit:
        pass
    else:
        AssertionError

def test_script_call_exception_test2():
    sys.argv[:] = origargs
    try:
        sys.argv.append("spam")
        main()
    except SystemExit:
        pass
    else:
        AssertionError

def test_script_call_capi():
    sys.argv[:] = origargs
    try:
        sys.argv.append("capi")
        main()
    except SystemExit:
        pass
    else:
        AssertionError


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
