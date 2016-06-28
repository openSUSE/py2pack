# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Thomas Bechtold <tbechtold@suse.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (see the file COPYING); if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import os
import shutil
import tempfile
import unittest
from ddt import ddt, data, unpack

import py2pack


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
