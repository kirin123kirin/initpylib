#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from os.path import exists, abspath, basename, dirname, join as pjoin
import argparse
from subprocess import getstatusoutput
import traceback
thisdir = dirname(__file__)
sep = os.sep

REPOHOME = "https://github.com/kirin123kirin"

POST_BUILD_AUTO_COMMANDS = f"""
git init
git clone https://github.com/kirin123kirin/.vscode.git
git add .
git commit -m "first commit"
git branch -M main
git remote add origin {REPOHOME}/{{pjname}}.git
git push -u origin main
"""

finishmsg_with_user_operation = f"""
Success `{{targetdir}}` Project Initialize.

if you wan't Git Management.

    cd {{targetdir}}
    {POST_BUILD_AUTO_COMMANDS}

OK Enjoy!
""".format

class PJtemplate(object):
    def __init__(self, argv=sys.argv):
        self.argv = argv
        self._args = None
        self.REPLACES_DICT = {}
        self.EXCLUDES = ["build", "dist", ".history", "initpylib.egg-info", "__pycache__", ".egg"]
        self._REPLACES_DICT_B = None

    @property
    def REPLACES_DICT_B(self):
        if not self._REPLACES_DICT_B:
            self._REPLACES_DICT_B = {k.encode(): v.encode() for k, v in self.REPLACES_DICT_B.items()}
        return self._REPLACES_DICT_B

    def replacer(self, dat):
        for k, v in self.REPLACES_DICT_B.items():
            dat = dat.replace(k, v)
        return dat

    def replacer_first(self, dat):
        for k, v in self.REPLACES_DICT.items():
            return dat.replace(k, v)

    def rencopy_all(self, srcdir, targetdir, add_skip_dirs=[]):
        excludes = self.EXCLUDES + add_skip_dirs
        excludes.sort(key=lambda x: len(x), reverse=True)

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

            for targetdir in dirs:
                if targetdir in excludes:
                    continue

                abstardir = pjoin(parent, targetdir)
                abstardir = self.replacer_first(abstardir)

                if not exists(abstardir):
                    os.mkdir(abstardir)

            for f in files:
                abstarfile = pjoin(parent, f)
                abstarfile = self.replacer_first(abstarfile)

                with open(pjoin(root, f), "rb") as r, open(abstarfile, "wb") as w:
                    w.write(self.replacer(r.read()))

    def _command(self, cmd):
        code, dat = getstatusoutput(cmd)
        if code == 0:
            if not self.args.quit:
                print("Run: {cmd}")
            return dat
        else:
            raise RuntimeError(f"Fail command {cmd}.\nreturn code: {code}\nreturn value:{dat}")

    def run(self):
        a = self.args
        if not exists(a.targetdir):
            os.makedirs(a.targetdir)

        self.rencopy_all(a.common, a.targetdir, [a.pjname])
        self.rencopy_all(a.srcdir, a.targetdir)

        if a.gitroot:
            os.chdir(a.targetdir)
            for cmd in POST_BUILD_AUTO_COMMANDS.splitlines():
                self._command(cmd.format(pjname=a.pjname))
            if not a.quit:
                print("Finished git initialize.")
        else:
            shutil.copytree(pjoin(thisdir, "..", ".vscode"), pjoin(a.targetdir, ".vscode"))
            if not a.quit:
                print(finishmsg_with_user_operation(targetdir=a.targetdir, pjname=a.pjname))
        return a.targetdir

    @property
    def args(self):
        if self._args is None:
            ps = argparse.ArgumentParser(
                description='Build Python Some Project Template.',
                prog="initpy"
            )

            subps = ps.add_subparsers()

            def build_subps(subcmdname, help):
                subps_args = subps.add_parser(subcmdname, help=help)
                subps_args.set_defaults(template="templates_" + ("common" if subcmdname == "py" else subcmdname))
                subps_args.add_argument("new_projectpath",
                                        help="Build New Project Directory Path(default build in current directory)")

            build_subps("capi", "Build Python C/C++ Extension API Module Project")
            build_subps("py", "Build Pure Python Module Project")

            ps.add_argument("-g", "--gitinit", type=str,
                            help=f"build github new repository baseurl (default {REPOHOME})", default=REPOHOME)
            ps.add_argument("-q", "--quit", action="store_true",
                            help="stdout print quit mode. (default False)")

            self._args = ps.parse_args(self.argv)

            if hasattr(self._args, 'template'):
                srcdir = abspath(pjoin(thisdir, self._args.template))
                common = abspath(pjoin(thisdir, "templates_common"))
                if not exists(srcdir):
                    raise RuntimeError("Error exists Any Bugs.\nWhere Source Directory" + srcdir)
            else:
                ps.print_help()
                sys.exit(1)

            pjname = basename(self._args.new_projectpath)

            global REPLACES_DICT
            self.REPLACES_DICT.update({
                "_PLEASE_PYPROJECT_NAME_": pjname,
                "_PLEASE_EXECUTABLE_FILENAME_": pjname + ".exe" if os.name == "nt" else pjname,
            })

            self._args.pjname = pjname
            self._args.common = common
            self._args.srcdir = srcdir
            self._args.targetdir = self._args.new_projectpath
            self._args.gitroot = self._args.gitinit
        return self._args

def main(argv=sys.argv):
    orgdir = abspath(os.getcwd())
    try:
        targetdir = PJtemplate(argv).run()
        os.chdir(targetdir)
    except Exception:
        traceback.print_exc(file=sys.stderr)
    finally:
        os.chdir(orgdir)


if __name__ == "__main__":
    main()
