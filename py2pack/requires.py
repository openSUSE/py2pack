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
import sys

import pkg_resources
from six.moves import filter
from six.moves import map


def _requirement_filter_by_marker(req):
    """check if the requirement is satisfied by the marker"""
    if hasattr(req, 'marker') and req.marker:
        marker_env = {'python_version': '.'.join(map(str, sys.version_info[:2])), 'sys_platform': sys.platform}
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
