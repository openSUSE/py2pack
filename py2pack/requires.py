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
import sys
import tempfile
import textwrap


def _safe_eval(descr, code, fallback):
    try:
        return eval(code)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        code = re.sub("(?m)^", "  ", code)
        sys.stderr.write(
            textwrap.dedent("""\

            WARNING: Exception encountered:

              %s: %s

            whilst eval'ing code for '%s' parameter in setup.py:

            %s

            Try regenerating with the --run option.
            """) % (exc_type.__name__, exc_value, descr, code))
        return fallback


def _requires_from_setup_py(file):
    """read requirements from the setup.py file"""
    data = {}
    contents = six.u(file.read())
    fixme = "FIXME: failed to extract %s from setup.py"
    match = re.search("ext_modules", contents)
    if match:
        data["is_extension"] = True
    match = re.search("[(,]\s*scripts\s*=\s*(\[.*?\])", contents, flags=re.DOTALL)
    if match:
        data["scripts"] = \
            _safe_eval("scripts", match.group(1), [fixme % "scripts"])
    match = re.search("test_suite\s*=\s*(.*)", contents)
    if match:
        data["test_suite"] = \
            _safe_eval("test_suite", match.group(1), [fixme % "test_suite"])
    match = re.search("install_requires\s*=\s*(\[.*?\])", contents, flags=re.DOTALL)
    if match:
        data["install_requires"] = \
            _safe_eval("install_requires", match.group(1), [fixme % "install_requires"])
    match = re.search("extras_require\s*=\s*(\{.*?\})", contents, flags=re.DOTALL)
    if match:
        data["extras_require"] = \
            _safe_eval("extras_require", match.group(1), [fixme % "extras_require"])
    match = re.search("tests_require\s*=\s*(\{.*?\})", contents, flags=re.DOTALL)
    if match:
        data["tests_require"] = \
            _safe_eval("tests_require", match.group(1), [fixme % "tests_require"])
    match = re.search("data_files\s*=\s*(\[.*?\])", contents, flags=re.DOTALL)
    if match:
        data["data_files"] = \
            _safe_eval("data_files", match.group(1), [fixme % "data_files"])
    match = re.search('entry_points\s*=\s*(\{.*?\}|""".*?"""|".*?")', contents, flags=re.DOTALL)
    if match:
        data["entry_points"] = \
            _safe_eval("entry_points", match.group(1), [fixme % "entry_points"])
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
