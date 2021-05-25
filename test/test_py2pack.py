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

import os
import unittest
from ddt import ddt, data, unpack

import py2pack


@ddt
class Py2packTestCase(unittest.TestCase):
    def setUp(self):
        class Args:
            name = "py2pack"
            version = "0.4.4"
            source_url = None

        self.args = Args()

    @data(
        ('py2pack', 'py2pack-0.6.4.tar.gz',
         'https://files.pythonhosted.org/packages/source/'
         'p/py2pack/py2pack-0.6.4.tar.gz'),
        ("SQLAlchemy", 'SQLAlchemy-1.0.5.tar.gz',
         'https://files.pythonhosted.org/packages/source/'
         'S/SQLAlchemy/SQLAlchemy-1.0.5.tar.gz'),
    )
    @unpack
    def test__get_source_url(self, pypi_name, extension, expected_url):
        self.assertEqual(py2pack._get_source_url(pypi_name, extension),
                         expected_url)

    def test_list(self):
        py2pack.list_packages(self.args)

    def test_search(self):
        py2pack.search(self.args)

    def test_show(self):
        py2pack.show(self.args)

    def test_newest_download_url(self):
        py2pack.fetch_data(self.args)
        url = py2pack.newest_download_url(self.args)
        self.assertTrue("url" in url)
        self.assertTrue("filename" in url)
        filename = "{0}-{1}.tar.gz".format(self.args.name, self.args.version)
        self.assertEqual(url["filename"], filename)
        self.assertEqual(url["packagetype"], "sdist")

    @data(
        (None, [], "FIXME-UNKNOWN"),
        ("Apache-2.0", [], "Apache-2.0"),
        ("", [], "FIXME-UNKNOWN"),
        ("Apache 2.0", [], "Apache-2.0"),
        ("", ["License :: OSI Approved :: Apache Software License"], "Apache-2.0"),
        ("BSD", [], "BSD (FIXME:No SPDX)"),
    )
    @unpack
    def test_normalize_license(self, licenses, classifiers, expected_result):
        d = {'license': licenses, 'classifiers': classifiers}
        py2pack._normalize_license(d)
        self.assertEqual(d['license'], expected_result)

    @data(
        ([""], None),
        (["foobar"], None),
        (["foobar", "License :: OSI Approved :: Apache Software License"],
         "Apache Software License"),
    )
    @unpack
    def test_license_from_classifiers(self, value, expected):
        d = {'classifiers': value}
        self.assertEqual(py2pack._license_from_classifiers(d), expected)

    def test__quote_shell_metacharacters(self):
        self.assertEqual(py2pack._quote_shell_metacharacters("abc"), "abc")
        self.assertEqual(py2pack._quote_shell_metacharacters("abc&"), "'abc&'")

    def test__prepare_template_env(self):
        template_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), '..', 'py2pack', 'templates')
        env = py2pack._prepare_template_env(template_dir)
        self.assertTrue('opensuse.spec' in env.list_templates())
        self.assertTrue('parenthesize_version' in env.filters)
        self.assertTrue('basename' in env.filters)

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
            {'setup_requires': 'six  >=1.9,!=1.0  # comment\nfoobar>=0.1,>=0.5'},
            {'setup_requires': ['six >= 1.9', 'foobar >= 0.1']}
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
