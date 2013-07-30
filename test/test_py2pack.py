# -*- coding: utf-8 -*-
#
# Copyright (c) 2013, Sascha Peilicke <saschpe@gmx.de>
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

import py2pack


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
        self.assertIn("url", url)
        self.assertIn("filename", url)
        filename = "{0}-{1}.tar.gz".format(self.args.name, self.args.version)
        self.assertEqual(url["filename"], filename)
        self.assertEqual(url["packagetype"], "sdist")
