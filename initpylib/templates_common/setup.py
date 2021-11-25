#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from os.path import exists, dirname, join as pjoin
thisdir = dirname(__file__)

__version__ = open(pjoin(thisdir, "VERSION"), "r").read().strip()

import shutil
import argparse
from tools import updatebadge

# Please Setting ----------------------------------------------------------
# If you wan't install compiled scripts by C++ etc


PROJECT_NAME = '_PLEASE_PYPROJECT_NAME_'

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

is_test = 'pytest' in sys.argv or 'test' in sys.argv
# Other Setting to setup.cfg
setup(
    packages=[PROJECT_NAME],
    setup_requires=['pytest-runner>=2.0,<3dev'] if is_test else []
)
