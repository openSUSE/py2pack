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

"""Module containing utility functions that fit nowhere else."""

from typing import List  # noqa: F401, pylint: disable=unused-import
try:
    import tomllib as toml
except ModuleNotFoundError:
    import tomli as toml

import tarfile
import zipfile


def _get_archive_filelist(filename):
    # type: (str) -> List[str]
    """Extract the list of files from a tar or zip archive.

    Args:
        filename: name of the archive

    Returns:
        Sorted list of files in the archive, excluding './'

    Raises:
        ValueError: when the file is neither a zip nor a tar archive
        FileNotFoundError: when the provided file does not exist (for Python 3)
        IOError: when the provided file does not exist (for Python 2)
    """
    names = []  # type: List[str]
    if tarfile.is_tarfile(filename):
        with tarfile.open(filename) as tar_file:
            names = sorted(tar_file.getnames())
    elif zipfile.is_zipfile(filename):
        with zipfile.ZipFile(filename) as zip_file:
            names = sorted(zip_file.namelist())
    else:
        raise ValueError("Can not get filenames from '{!s}'. "
                         "Not a tar or zip file".format(filename))
    if "./" in names:
        names.remove("./")
    return names


def parse_pyproject(archive):
    """Parse the pyproject.toml in the archive and return the metadata as dict.

    Args:
        archive: the filename of the archive

    Returns:
        dict of metadata. Empty if no pyproject.toml was found in the toplevel directory
    """
    pyproject = {}
    if tarfile.is_tarfile(archive):
        with tarfile.open(archive) as tar_file:
            for m in tar_file:
                if m.name.endswith('pyproject.toml') and m.name.count("/") == 1:
                    with tar_file.extractfile(m) as fh:
                        pyproject = toml.load(fh)
                    break
    elif zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zip_file:
            for name in zip_file.namelist():
                if name.endswith('pyproject.toml') and name.count("/") == 1:
                    with zip_file.open(name) as fh:
                        pyproject = toml.load(fh)
                    break
    else:
        raise ValueError("Can not extract pyproject.toml from '{!s}'. "
                         "Not a tar or zip file".format(archive))
    return pyproject


def get_pyproject_table(data, key, notfound=None):
    """Return the contents of a toml table.

    Args:
        data: dict of toml contents
        key: period separated table name, e.g. "project.dependencies"
        notfound: return this if the table is not in data, None by default

    Returns:
        content of table (list or dict) or notfound
    """
    table = data
    for level in key.split("."):
        if level in table:
            table = table[level]
        else:
            return notfound
    return table
