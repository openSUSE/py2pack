# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Sascha Peilicke <sascha@peilicke.de>
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

    @data((None, ""), ("Apache-2.0", "Apache-2.0"), ("", ""))
    @unpack
    def test_normalize_license(self, value, expected_result):
        d = {'license': value}
        py2pack._normalize_license(d)
        self.assertEqual(d['license'], expected_result)

    @data(
        (
            {'install_requires': ['six', 'monotonic>=0.1']},
            {'install_requires': ['six', 'monotonic >= 0.1']},
        ),
        (
            {'install_requires': ['six', 'foobar>=0.1,>=0.5']},
            {'install_requires': ['six', 'foobar >= 0.1']},
        ),
        (
            {'install_requires': ['six  >=1.9', 'foobar>=0.1,>=0.5']},
            {'install_requires': ['six >= 1.9', 'foobar >= 0.1']}
        ),
        (
            {'extras_require': {'extra1': ['foobar<=3.0, >= 2.1']}},
            {'extras_require': {'extra1': ['foobar >= 2.1']}}
        )
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
        )
    )
    @unpack
    def test_canonicalize_setup_data_console_scripts(self, data, expected_data):
        py2pack._canonicalize_setup_data(data)
        self.assertEqual(list(data['console_scripts']), expected_data)
