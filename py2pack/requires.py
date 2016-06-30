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
import pkg_resources
from six.moves import filter
from six.moves import map
import subprocess
import tempfile


def _set_source_encoding_utf8(setup_py_file):
    """set a encoding header as suggested in PEP-0263. This
    is not entirely correct because we don't know the encoding of the
    given file but it's at least a chance to get metadata from the setup.py"""
    with open(setup_py_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("# -*- coding: utf-8 -*-\n" + content)


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
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError:
            # try again with a encoding in setup.py
            _set_source_encoding_utf8("setup.py")
            subprocess.check_output(cmd, shell=True)

        with open(tempfile_json.name, "r") as f:
            data = json.loads(f.read())
    finally:
        os.chdir(current_cwd)
    return data


def _requirement_filter_by_marker(req):
    """check if the requirement is satisfied by the marker"""
    if hasattr(req, 'marker') and req.marker:
        # TODO (toabctl): currently we hardcode python 2.7 and linux2
        # see https://www.python.org/dev/peps/pep-0508/#environment-markers
        marker_env = {'python_version': '2.7', 'sys_platform': 'linux'}
        if not req.marker.evaluate(environment=marker_env):
            return False
    return True


def _requirement_find_lowest_possible(req):
        """ find lowest required version"""
        version_dep = None
        version_comp = None
        for dep in req.specs:
            version = pkg_resources.parse_version(dep[1])
            # we don't want to have a not supported version as minimal version
            if dep[0] == '!=':
                continue
            # try to use the lowest version available
            # i.e. for ">=0.8.4,>=0.9.7", select "0.8.4"
            if (not version_dep or
                    version < pkg_resources.parse_version(version_dep)):
                version_dep = dep[1]
                version_comp = dep[0]
        return filter(lambda x: x is not None,
                      [req.unsafe_name, version_comp, version_dep])


def _requirements_sanitize(req_list):
    filtered_req_list = map(
        _requirement_find_lowest_possible, filter(
            _requirement_filter_by_marker,
            map(lambda x: pkg_resources.Requirement.parse(x), req_list)
        )
    )
    return [" ".join(req) for req in filtered_req_list]
