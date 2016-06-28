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

import distutils.core
import os
import re
import setuptools.sandbox
import shutil
import six
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
    match = re.search("data_files\s*=\s*(\[.*?\])", contents, flags=re.DOTALL)
    if match:
        data["data_files"] = eval(match.group(1))
    match = re.search('entry_points\s*=\s*(\{.*?\}|""".*?"""|".*?")', contents, flags=re.DOTALL)
    if match:
        data["entry_points"] = eval(match.group(1))
    return data


def _requires_from_setup_py_run(tar_file, setup_filename):
    """run setup.py from a tarfile in a setuptools sandbox"""
    tempdir = tempfile.mkdtemp()
    setuptools.sandbox.DirectorySandbox(tempdir).run(lambda: tar_file.extractall(tempdir))

    setup_filename = os.path.join(tempdir, setup_filename)
    distutils.core._setup_stop_after = "config"
    setuptools.sandbox.run_setup(setup_filename, "")
    dist = distutils.core._setup_distribution
    shutil.rmtree(tempdir)

    data = {}
    if dist.ext_modules:
        data["is_extension"] = True
    if dist.scripts:
        data["scripts"] = dist.scripts
    if dist.test_suite:
        data["test_suite"] = dist.test_suite
    if dist.install_requires:
        data["install_requires"] = dist.install_requires
    if dist.extras_require:
        data["extras_require"] = dist.extras_require
    if dist.data_files:
        data["data_files"] = dist.data_files
    if dist.entry_points:
        data["entry_points"] = dist.entry_points
    return data
