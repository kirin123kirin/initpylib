#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from os.path import exists, dirname, join as pjoin
thisdir = dirname(__file__)

__version__ = open(pjoin(thisdir, "VERSION"), "r").read().strip()

import shutil
import argparse
from tools import updatebadge

from distutils.dist import Distribution

# setup.cfg metadata Infomation (`meta` of py dictionary)
_dt = Distribution()
_dt.parse_config_files()
_dt.parse_command_line()
_meta = _dt.get_option_dict('metadata')
def meta(s):
    return _meta[s][1]

# Please Setting ----------------------------------------------------------
# If you wan't install compiled scripts by C++ etc


PROJECT_NAME = meta("name")

# -------------------------------------------------------------------------

from setuptools import setup

ps = argparse.ArgumentParser()
ps.add_argument('-f', '--force', action="store_true", dest="is_force")
ps.add_argument('-g', '--debug', action="store_true", dest="is_debug")
ps.add_argument('--build-type', default="Release")
arg = ps.parse_known_args(sys.argv)[0]

if arg.is_force:
    for d in ["build", "dist", PROJECT_NAME + ".egg-info"]:
        if exists(pjoin(thisdir, d)):
            shutil.rmtree(pjoin(thisdir, d))

# Readme badge link update.
updatebadge.readme(pjoin(thisdir, "README.md"), new_version=__version__)

# Other Setting to setup.cfg
is_test = 'pytest' in sys.argv or 'test' in sys.argv
setup(setup_requires=['pytest-runner>=2.0,<3dev'] if is_test else [])
