#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, Sebastian Wagner <sebix@sebix.at>
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

import datetime
import os
import os.path
import pwd
import sys
import unittest

import pytest

import py2pack


class Args(object):
    run = False
    template = ''
    filename = ''
    name = 'py2pack'
    version = '0.8.5'
    source_url = None


compare_dir = os.path.join(os.path.dirname(__file__), 'examples')
maxDiff = None
username = pwd.getpwuid(os.getuid())[4]


@pytest.mark.parametrize('template, fetch_tarball',
                         [('fedora.spec', False),
                          ('mageia.spec', False),
                          ('opensuse-legacy.spec', False),
                          ('opensuse.dsc', False),
                          ('opensuse.spec', False),
                          ('opensuse.spec', True)])
def test_template(tmpdir, template, fetch_tarball):
    """ Test if generated specfile equals to stored one. """
    if (template, fetch_tarball, sys.version_info[:2]) == ('opensuse.spec', True, (3, 6)):
        raise unittest.SkipTest('This combination of tests fails ATM.')
    args = Args()
    args.template = template
    base, ext = template.split(".")
    suffix = '-augmented' if fetch_tarball else ''
    filename = "{}{}.{}".format(base, suffix, ext)
    args.filename = filename
    with tmpdir.as_cwd():
        if fetch_tarball:
            py2pack.fetch(args)
            py2pack.generate(args)
        else:
            with pytest.warns(UserWarning, match="No tarball"):
                py2pack.generate(args)
        with open(filename) as filehandle:
            written_spec = filehandle.read()
    reference = os.path.join(compare_dir, 'py2pack-{}'.format(filename))
    with open(reference) as filehandle:
        required = filehandle.read()
    required = required.replace('__USER__', username, 1)
    required = required.replace('__YEAR__', str(datetime.date.today().year), 1)
    assert written_spec == required
