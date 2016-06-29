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

import os
import shutil
import tempfile
import unittest
from ddt import ddt, data, unpack

import py2pack
import py2pack.utils


@ddt
class Py2packRequiresTestCase(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='py2pack_test_')
        self.setup_py = os.path.join(self.tmpdir, 'setup.py')

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_setup_py(self, content):
        with open(self.setup_py, 'w+') as f:
            f.write(content)

    def test__requires_from_setup_py_pbr(self):
        self._write_setup_py("""
setuptools.setup(
    setup_requires=['pbr'],
    pbr=True)
""")
        with open(self.setup_py) as f:
            data = py2pack.requires._requires_from_setup_py(f)
        self.assertEqual(data, {})

    @data(
        ("[]", []),
        ("['req1>=1,<2', 'req2']", ['req1>=1,<2', 'req2']),
        ("""['req1',
        'req2']""", ['req1', 'req2']),
    )
    @unpack
    def test__requires_from_setup_py_install_requires(self, req, expected_req):
        self._write_setup_py("""
setuptools.setup(
    install_requires=%s,
        )""" % req)
        with open(self.setup_py) as f:
            data = py2pack.requires._requires_from_setup_py(f)
        self.assertEqual(data, {'install_requires': expected_req})

    @data(
        ("{}", {}),
        ("{'ssh': ['paramiko']}", {'ssh': ['paramiko']}),
        ("""{'ssh':
        # a comment
        ['paramiko']}""", {'ssh': ['paramiko']}),
    )
    @unpack
    def test__requires_from_setup_py_extras_require(self, req, expected_req):
        self._write_setup_py("""
setuptools.setup(
    extras_require=%s,
        )""" % req)
        with open(self.setup_py) as f:
            data = py2pack.requires._requires_from_setup_py(f)
        self.assertEqual(data, {'extras_require': expected_req})

    @data(
        ("{}", {}),
        ("{'ssh': ['paramiko']}", {'ssh': ['paramiko']}),
        ("""{'ssh':
        # a comment
        ['paramiko']}""", {'ssh': ['paramiko']}),
    )
    @unpack
    def test__requires_from_setup_py_tests_require(self, req, expected_req):
        self._write_setup_py("""
setuptools.setup(
    tests_require=%s,
        )""" % req)
        with open(self.setup_py) as f:
            data = py2pack.requires._requires_from_setup_py(f)
        self.assertEqual(data, {'tests_require': expected_req})

    @data(
        ("{}", {}),
        ("{'console_scripts':['script1=pkg:main']}",
         {'console_scripts': ['script1=pkg:main']}),
        ("{'console_scripts':\n#a comment\n['script1=\\\npkg:main']}",
         {'console_scripts': ['script1=pkg:main']}),
        ("{'console_scripts' : [\n'foo = foo.interface:cli',\n]}",
         {'console_scripts': ['foo = foo.interface:cli']}),
        # entry_points can also be a .ini style section
        ('"""\n[console_scripts]\nfoo = bar\n"""', '\n[console_scripts]\nfoo = bar\n'),
    )
    @unpack
    def test__requires_from_setup_py_entry_points(self, req, expected_req):
        self._write_setup_py("""
setuptools.setup(
    entry_points=%s,
        )""" % req)
        with open(self.setup_py) as f:
            data = py2pack.requires._requires_from_setup_py(f)
        self.assertEqual(data, {'entry_points': expected_req})

    def test__requires_from_setup_py_run(self):
        self._write_setup_py("""
import setuptools
setuptools.setup(
    name='testpkg',
    install_requires=['foo', 'bar'],
)
""")
        data = py2pack.requires._requires_from_setup_py_run(self.tmpdir)
        self.assertEqual(data, {'install_requires': ['foo', 'bar']})

    def test__requires_from_setup_py_run_with_variables(self):
        self._write_setup_py("""
import setuptools
req = ['foo', 'bar']
test_req = ['test']
setuptools.setup(
    name='testpkg',
    install_requires=req,
    tests_require=test_req
)
""")
        data = py2pack.requires._requires_from_setup_py_run(self.tmpdir)
        self.assertEqual(data, {'install_requires': ['foo', 'bar'],
                                'tests_require': ['test']})
