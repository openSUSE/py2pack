#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Thomas Bechtold <tbechtold@suse.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Generate packages from pypi on the openbuildservice
# The script needs a installed "osc" (the CLI for OBS)
#
# THIS IS ONLY USEFUL FOR TESTING!!!!

from __future__ import print_function

import argparse
import os

import sh


OBS_API = 'https://api.opensuse.org'


def main():
    parser = argparse.ArgumentParser(
        description='create OBS packages from pypi')
    parser.add_argument('--pypi-names', help='pypi package names to add to OBS',
                        nargs='*', default=[])
    parser.add_argument('workdir', help='some temp dir to do OBS checkout')
    parser.add_argument('obsproject', help='OBS project name')
    args = parser.parse_args()

    olddir = os.getcwd()
    os.chdir(args.workdir)

    osc = sh.Command('osc')
    py2pack = sh.Command('py2pack')

    obs_project_path = os.path.join(args.workdir, args.obsproject)
    if not os.path.exists(obs_project_path):
        osc('checkout', '%s' % (args.obsproject))
    os.chdir(obs_project_path)

    for pkg in args.pypi_names:
        print('packaging %s ...' % pkg)
        obs_pkg = 'python-%s' % pkg
        obs_pkg_path = os.path.join(obs_project_path, obs_pkg)
        if not os.path.exists(obs_pkg_path):
            osc('mkpac', obs_pkg)
        os.chdir(obs_pkg_path)
        py2pack('fetch', pkg)
        py2pack('generate', pkg, '-f', '%s.spec' % obs_pkg)
        osc('vc', '-m', 'Automatic package creation with py2pack')
        osc('addremove')
        osc('commit', '-m', 'Automatic package creation with py2pack')
        os.chdir(obs_project_path)

    os.chdir(olddir)


if __name__ == '__main__':
    main()
