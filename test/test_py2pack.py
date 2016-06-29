#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Sascha Peilicke <sascha@peilicke.de>
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

import pkg_resources
import unittest
from ddt import ddt, data, unpack

import py2pack


@ddt
class Py2packTestCase(unittest.TestCase):
    def setUp(self):
        class Args:
            name = "py2pack"
            version = "0.4.4"

        self.args = Args()

    def test_list(self):
        py2pack.list(self.args)

    def test_search(self):
        py2pack.search(self.args)

    def test_show(self):
        py2pack.show(self.args)

    def test_newest_download_url(self):
        url = py2pack.newest_download_url(self.args)
        self.assertTrue("url" in url)
        self.assertTrue("filename" in url)
        filename = "{0}-{1}.tar.gz".format(self.args.name, self.args.version)
        self.assertEqual(url["filename"], filename)
        self.assertEqual(url["packagetype"], "sdist")

    @data((None, ""), ("Apache-2.0", "Apache-2.0"), ("", ""),
          ("Apache 2.0", "Apache-2.0"))
    @unpack
    def test_normalize_license(self, value, expected_result):
        d = {'license': value}
        py2pack._normalize_license(d)
        self.assertEqual(d['license'], expected_result)

    @data(
        ("pywin32>=1.0;sys_platform=='win32'  # PSF", False),
        ("foobar", True),
        ("foobar;python_version=='2.7'", True),
        ("foobar;python_version=='3.5'", False),
    )
    @unpack
    def test__requirement_filter_by_marker(self, req, expected):
        pkg = pkg_resources.Requirement.parse(req)
        self.assertEqual(py2pack._requirement_filter_by_marker(pkg), expected)

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
        self.assertEqual(list(py2pack._requirement_find_lowest_possible(pkg)), expected)

    @data(
        (['six', 'monotonic>=0.1'], ['six', 'monotonic >= 0.1']),
        (['monotonic>=1.0,>0.1'], ['monotonic > 0.1']),
    )
    @unpack
    def test__requirements_sanitize(self, req_list, expected):
        self.assertEqual(py2pack._requirements_sanitize(req_list), expected)

    @data(
        (
            {'install_requires': ["pywin32>=1.0;sys_platform=='win32'", 'monotonic>=0.1 #comment']},
            {'install_requires': ['monotonic >= 0.1']},
        ),
        (
            {'install_requires': 'six  >=1.9,!=1.0  # comment\nfoobar>=0.1,>=0.5'},
            {'install_requires': ['six >= 1.9', 'foobar >= 0.1']}
        ),
        (
            {'tests_require': ['six  >=1.9', 'foobar>=0.1,>=0.5']},
            {'tests_require': ['six >= 1.9', 'foobar >= 0.1']}
        ),
        (
            {'tests_require': 'six  >=1.9\nfoobar>=0.1,>=0.5'},
            {'tests_require': ['six >= 1.9', 'foobar >= 0.1']}
        ),
        (
            {'extras_require': {'extra1': ['foobar<=3.0, >= 2.1']}},
            {'extras_require': {'extra1': ['foobar >= 2.1']}}
        ),
        (
            {'extras_require': {'extra1': 'foobar<=3.0, >= 2.1\ntest1  # comment',
                                'extra2': ['test2']}},
            {'extras_require': {'extra1': ['foobar >= 2.1', 'test1'],
                                'extra2': ['test2']}}
        ),
    )
    @unpack
    def test_canonicalize_setup_data(self, data, expected_data):
        py2pack._canonicalize_setup_data(data)
        self.assertEqual(data, expected_data)

    @data(
        (
            {'entry_points': "[console_scripts]\nfoo = foo:main"},
            ['foo']
        ),
        (
            {'entry_points': "[console_scripts]\nfoo = foo:main\n\nbar=abc:xyz"},
            ['foo', 'bar']
        ),
        (
            {'entry_points': {'console_scripts': ['foo = foo:main',
                                                  'bar=bar:main']}},
            ['foo', 'bar']
        )
    )
    @unpack
    def test_canonicalize_setup_data_console_scripts(self, data, expected_data):
        py2pack._canonicalize_setup_data(data)
        self.assertEqual(sorted(list(data['console_scripts'])),
                         sorted(expected_data))
