#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from os.path import exists, abspath, basename, dirname, join as pjoin

REPKEY = "_PLEASE_PYPROJECT_NAME_"
REPKEY_B = REPKEY.encode()

REPOHOME = "https://github.com/kirin123kirin"

pjname = None
pjname_B = None

sep = os.sep

def rencopy_contents(srcpath, targetpath):
    with open(srcpath, "rb") as r, open(targetpath, "wb") as w:
        content = r.read()
        if REPKEY_B in content:
            w.write(content.replace(REPKEY_B, pjname.encode()))
        else:
            w.write(content)

def rencopy_all(srcdir, targetdir):
    excludes = ["build", "dist", ".history", "initpylib.egg-info", "__pycache__"]

    def is_skip(f):
        for e in excludes:
            e = sep + e
            if f.endswith(e) or e + sep in f:
                return True
        return False

    for root, dirs, files in os.walk(srcdir):
        parent = root.replace(srcdir, targetdir)
        if is_skip(parent):
            continue

        for d in dirs:
            if d in excludes:
                continue
            childdir = pjoin(parent, d).replace(REPKEY, pjname)
            if not exists(childdir):
                os.mkdir(childdir)

        for f in files:
            targetpath = pjoin(parent, f).replace(REPKEY, pjname)
            rencopy_contents(pjoin(root, f), targetpath)


finishmsg = """
Success `{targetdir}` Project Initialize.

if you wan't Git Management.

    cd {targetdir}
    git init
    git add .
    git submodule update -i
    git commit -m "first commit"
    git branch -M main
    git remote add origin {REPOHOME}/{pjname}.git
    git push -u origin main  #-> Input git hub Username, Password

OK Enjoy!
"""


def main():
    import argparse
    ps = argparse.ArgumentParser(
        description='Build Python Some Project Template.',
        prog="initpy"
    )

    subps = ps.add_subparsers()

    def build_subps(subcmdname, help):
        subps_args = subps.add_parser(subcmdname, help=help)
        subps_args.set_defaults(template="templates_" + subcmdname)
        subps_args.add_argument("new_projectpath",
                                help="Build New Project Directory Path(default build in current directory)")

    build_subps("capi", "Build Python C/C++ Extension API Module Project")

    args = ps.parse_args()

    thisdir = dirname(__file__)
    if hasattr(args, 'template'):
        srcdir = abspath(pjoin(thisdir, args.template))
        if not exists(srcdir):
            raise RuntimeError("Error exists Any Bugs..")
    else:
        ps.print_help()
        sys.exit(1)

    targetdir = args.new_projectpath
    if not exists(targetdir):
        os.makedirs(targetdir)

    global pjname, pjname_B
    pjname = basename(targetdir)
    pjname_B = pjname.encode()

    rencopy_all(srcdir, targetdir)

    print(finishmsg.format(targetdir=targetdir, REPOHOME=REPOHOME, pjname=pjname))


if __name__ == "__main__":
    main()
