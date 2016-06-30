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
import pkg_resources
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

    def test__set_source_encoding_utf8(self):
        self._write_setup_py("")
        py2pack.requires._set_source_encoding_utf8(self.setup_py)
        with open(self.setup_py, 'r') as f:
            self.assertEqual(f.read(), "# -*- coding: utf-8 -*-\n")

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

    def test__requires_from_setup_py_run_distutils(self):
        self._write_setup_py("""# -*- coding: utf8 -*-
from distutils.core import setup
setup(
    version="0.3.1",
    author="的å",
    package_dir={"": "test"},
    py_modules=["test"],
    scripts=[
        "bin/test",
        ]
)
""")
        data = py2pack.requires._requires_from_setup_py_run(self.tmpdir)
        self.assertEqual(data, {'scripts': ['bin/test']})

    def test__requires_from_setup_py_run_unknown_encoding(self):
        self._write_setup_py("""
from distutils.core import setup
setup(
    version="0.3.1",
    author="的å",
    package_dir={"": "test"},
    py_modules=["test"],
    scripts=[
        "bin/test",
        ]
)
""")
        data = py2pack.requires._requires_from_setup_py_run(self.tmpdir)
        self.assertEqual(data, {'scripts': ['bin/test']})

    @data(
        ("pywin32>=1.0;sys_platform=='win32'  # PSF", False),
        ("foobar", True),
        ("foobar;python_version=='2.7'", True),
        ("foobar;python_version=='3.5'", False),
    )
    @unpack
    def test__requirement_filter_by_marker(self, req, expected):
        pkg = pkg_resources.Requirement.parse(req)
        self.assertEqual(py2pack.requires._requirement_filter_by_marker(pkg), expected)

    @data(
        ("foobar>=1.0", ["foobar", ">=", "1.0"]),
        ("foobar>=1.0,>2", ["foobar", ">=", "1.0"]),
        ("foobar>=2,>1.0,<=3", ["foobar", ">", "1.0"]),
        ("foobar>=2,>1.0,!=0.5", ["foobar", ">", "1.0"]),
        ("foobar!=0.5", ["foobar"]),
    )
    @unpack
    def test__requirement_find_lowest_possible(self, req, expected):
        pkg = pkg_resources.Requirement.parse(req)
        self.assertEqual(list(py2pack.requires._requirement_find_lowest_possible(pkg)), expected)

    @data(
        (['six', 'monotonic>=0.1'], ['six', 'monotonic >= 0.1']),
        (['monotonic>=1.0,>0.1'], ['monotonic > 0.1']),
    )
    @unpack
    def test__requirements_sanitize(self, req_list, expected):
        self.assertEqual(py2pack.requires._requirements_sanitize(req_list), expected)
