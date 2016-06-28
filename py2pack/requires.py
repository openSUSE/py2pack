# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Thomas Bechtold <tbechtold@suse.com>
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

from __future__ import absolute_import
from __future__ import print_function

import re


def _requires_from_setup_py(file):
    """read requirements from the setup.py file"""
    data = {}
    contents = file.read().decode('utf-8')
    match = re.search("ext_modules", contents)
    if match:
        data["is_extension"] = True
    match = re.search("[(,]\s*scripts\s*=\s*(\[.*?\])", contents, flags=re.DOTALL)
    if match:
        data["scripts"] = eval(match.group(1))
    match = re.search("test_suite\s*=\s*(.*)", contents)
    if match:
        data["test_suite"] = eval(match.group(1))
    match = re.search("install_requires\s*=\s*(\[.*?\])", contents, flags=re.DOTALL)
    if match:
        data["install_requires"] = eval(match.group(1))
    match = re.search("extras_require\s*=\s*(\{.*?\})", contents, flags=re.DOTALL)
    if match:
        data["extras_require"] = eval(match.group(1))
    match = re.search("data_files\s*=\s*(\[.*?\])", contents, flags=re.DOTALL)
    if match:
        data["data_files"] = eval(match.group(1))
    match = re.search('entry_points\s*=\s*(\{.*?\}|""".*?"""|".*?")', contents, flags=re.DOTALL)
    if match:
        data["entry_points"] = eval(match.group(1))
    return data
