#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010, Sascha Peilicke <saschpe@gmx.de>
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
import doctest

import py2pack


class Test(unittest.TestCase):
    """Unit tests for py2pack."""

    def test_doctests(self):
        """Run py2pack doctests"""
        doctest.testmod(py2pack)

if __name__ == "__main__":
    unittest.main()
