# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Thomas Bechtold <tbechtold@suse.com>
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

from __future__ import absolute_import
from __future__ import print_function

import json
import os
import re
import six
import subprocess
import tempfile


def _requires_from_setup_py(file):
    """read requirements from the setup.py file"""
    data = {}
    contents = six.u(file.read())
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
    match = re.search("tests_require\s*=\s*(\{.*?\})", contents, flags=re.DOTALL)
    if match:
        data["tests_require"] = eval(match.group(1))
    match = re.search("data_files\s*=\s*(\[.*?\])", contents, flags=re.DOTALL)
    if match:
        data["data_files"] = eval(match.group(1))
    match = re.search('entry_points\s*=\s*(\{.*?\}|""".*?"""|".*?")', contents, flags=re.DOTALL)
    if match:
        data["entry_points"] = eval(match.group(1))
    return data


def _requires_from_setup_py_run(tmp_dir):
    """run the get_metadata command via the setup.py in the given tmp_dir.
    the output of get_metadata is json and is stored in a tempfile
    which is then read in and returned as data"""
    data = {}
    try:
        current_cwd = os.getcwd()
        tempfile_json = tempfile.NamedTemporaryFile()
        # if there is a single subdir, enter that one
        dir_list = os.listdir(tmp_dir)
        if len(dir_list) == 1 and os.path.isdir(dir_list[0]):
            os.chdir(os.path.join(tmp_dir, dir_list[0]))
        else:
            os.chdir(tmp_dir)
        # generate a temporary json file which contains the metadata
        cmd = "python setup.py -q --command-packages py2pack " \
              "get_metadata -o %s " % tempfile_json.name
        subprocess.check_output(cmd, shell=True)
        with open(tempfile_json.name, "r") as f:
            data = json.loads(f.read())
    finally:
        os.chdir(current_cwd)
    return data
