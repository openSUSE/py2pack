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

""" Module for handling entries from requirements.txt

This module contains internal functions to sanitize requirement entries and
bring them into a form that can be directly included in a spec file.

For further information concerning requirements (and markers), see `PEP 508
<https://www.python.org/dev/peps/pep-0508/>`. For versions, see `PEP 440
<https://www.python.org/dev/peps/pep-0440/>`
"""

from typing import List, Optional  # noqa: F401, pylint: disable=unused-import
import sys

import pkg_resources


def _requirement_filter_by_marker(req):
    # type: (pkg_resources.Requirement) -> bool
    """Check if the requirement is satisfied by the marker.

    This function checks for a given Requirement whether its environment marker
    is satisfied on the current platform. Currently only the python version and
    system platform are checked.
    """
    if hasattr(req, 'marker') and req.marker:
        marker_env = {
            'python_version': '.'.join(map(str, sys.version_info[:2])),
            'sys_platform': sys.platform
        }
        if not req.marker.evaluate(environment=marker_env):
            return False
    return True


def _requirement_find_lowest_possible(req):
    # type: (pkg_resources.Requirement) -> List[str]
    """Find lowest required version.

    Given a single Requirement, this function calculates the lowest required
    version to satisfy it. If the requirement excludes a specific version, then
    this version will not be used as the minimal supported version.

    Examples
    --------

    >>> req = pkg_resources.Requirement.parse("foobar>=1.0,>2")
    >>> _requirement_find_lowest_possible(req)
    ['foobar', '>=', '1.0']
    >>> req = pkg_resources.Requirement.parse("baz>=1.3,>3,!=1.5")
    >>> _requirement_find_lowest_possible(req)
    ['baz', '>=', '1.3']

    """
    version_dep = None  # type: Optional[str]
    version_comp = None  # type: Optional[str]
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

    assert (version_dep is None and version_comp is None) or \
        (version_dep is not None and version_comp is not None)

    return [
        x for x in (req.unsafe_name, version_comp, version_dep)
        if x is not None]


def _requirements_sanitize(req_list):
    # type: (List[str]) -> List[str]
    """
    Cleanup a list of requirement strings (e.g. from requirements.txt) to only
    contain entries valid for this platform and with the lowest required version
    only.

    Example
    -------

    >>> from sys import version_info
    >>> _requirements_sanitize([
    ...     'foo>=3.0',
    ...     "monotonic>=1.0,>0.1;python_version=='2.4'",
    ...     "bar>1.0;python_version=='{}.{}'".format(version_info[0], version_info[1])
    ... ])
    ['foo >= 3.0', 'bar > 1.0']
    """
    filtered_req_list = (
        _requirement_find_lowest_possible(req) for req in
        (pkg_resources.Requirement.parse(s) for s in req_list)
        if _requirement_filter_by_marker(req)
    )
    return [" ".join(req) for req in filtered_req_list]
