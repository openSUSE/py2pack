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

import os
import os.path
import pwd
import tempfile
import unittest

import py2pack


class Args(object):
    run = False
    template = ''
    filename = ''
    name = 'py2pack'
    version = '0.8.0'
    source_url = None


def generate_template_function(template):
    def test_template(self):
        """ Test if generated specfile for %s equals to stored one. """ % template
        args = Args()
        args.template = template
        with tempfile.NamedTemporaryFile(mode='w+t') as filehandle:
            filename = filehandle.name
            args.filename = filename
            py2pack.generate(args)
            filehandle.seek(0)
            written_spec = filehandle.read()
        with open(os.path.join(self.compare_dir, 'py2pack-%s' % template)) as filehandle:
            required = filehandle.read()
        required = required.replace('__USER__', self.username, 1)
        self.assertEqual(written_spec, required)
    return test_template


class TemplateTestCase(unittest.TestCase):
    compare_dir = os.path.join(os.path.dirname(__file__), 'examples')
    maxDiff = None
    username = pwd.getpwuid(os.getuid())[4]


for template in ('fedora.spec', 'mageia.spec', 'opensuse-legacy.spec', 'opensuse.dsc', 'opensuse.spec'):
    setattr(TemplateTestCase,
            'test_template_%s' % template,
            generate_template_function(template))
