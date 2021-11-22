#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from tempfile import TemporaryDirectory
from main import main

origargs = sys.argv.copy()

def test_script_call_capi_ok_test():
    sys.argv[:] = origargs
    tmpdir = TemporaryDirectory()
    sys.argv.extend(["capi", tmpdir.name])
    main()
    tmp_n = sum(len(dirs) + len(files) for _, dirs, files in os.walk("templates_capi"))
    build_n = sum(len(dirs) + len(files) for _, dirs, files in os.walk(tmpdir.name))
    assert(build_n >= tmp_n)

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

