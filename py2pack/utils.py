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

import os
import tempfile
import shutil
from contextlib import contextmanager
from build.util import project_wheel_metadata

from typing import List  # noqa: F401, pylint: disable=unused-import
try:
    import tomllib as toml
except ModuleNotFoundError:
    import tomli as toml

import tarfile
import zipfile
from sys import getsizeof, maxsize
from typing import Any
from typing import Collection
from typing import Dict
from typing import Hashable
from typing import ItemsView
from typing import Iterator
from typing import KeysView
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import ValuesView
from typing import cast
from backports.entry_points_selectable import EntryPoint, EntryPoints
from email import parser
from importlib import metadata
import json
from io import StringIO


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


def get_setuptools_scripts(data):
    """parse setuptools entry_points and return all script names.

    Setuptools style entry_points as returned by metaextract may be
    a string with .ini-style sections or a dict

    (The PEP518 projects.entry-points table does not have scripts subtables.)

    Args:
        data: dict of metadata

    Returns:
        list of script names
    """
    entry_points = data.get('entry_points', None)
    if isinstance(entry_points, str):
        eps = EntryPoints(EntryPoints._from_text(entry_points))
    elif isinstance(entry_points, dict):
        eps = EntryPoints([EntryPoint(*map(str.strip, entry.split("=", 1)), groupname)
                           for groupname, group in entry_points.items()
                           for entry in group
                           if groupname in ["console_scripts", "gui_scripts"]])
    else:
        return []
    scripts = (list(eps.select(group="console_scripts").names) +
               list(eps.select(group="gui_scripts").names))
    return scripts


@contextmanager
def _extract_to_tempdir(archive_filename):
    """extract the given tarball or zipfile to a tempdir and change
    the cwd to the new tempdir. Delete the tempdir at the end"""
    if not os.path.exists(archive_filename):
        raise Exception("Archive '%s' does not exist" % (archive_filename))

    tempdir = tempfile.mkdtemp(prefix="py2pack_")
    current_cwd = os.getcwd()
    try:
        if tarfile.is_tarfile(archive_filename):
            with tarfile.open(archive_filename) as f:
                f.extractall(tempdir)
        elif zipfile.is_zipfile(archive_filename):
            with zipfile.ZipFile(archive_filename) as f:
                f.extractall(tempdir)
        else:
            raise Exception("Can not extract '%s'. "
                            "Not a tar or zip file" % archive_filename)
        os.chdir(tempdir)
        yield tempdir
    finally:
        os.chdir(current_cwd)
        shutil.rmtree(tempdir)


def get_metadata(filename):
    """
    Extracts metadata from the archive filename
    """
    data = {}

    with _extract_to_tempdir(filename) as root_dir:
        dir_list, *_ = os.listdir(root_dir)
        path = os.path.join(root_dir, dir_list)
        mdata = project_wheel_metadata(path, isolated=True)

        data['home_page'] = mdata.get('Home-page')
        data['name'] = mdata.get('Name')
        data['version'] = mdata.get('Version')
        data['description'] = mdata.get('Description')
        data['summary'] = mdata.get('Summary')
        data['license'] = mdata.get('License')
        data['keywords'] = mdata.get('Keywords')
        data['author'] = mdata.get('Author')
        data['author_email'] = mdata.get('Author-email')
        data['maintainer'] = mdata.get('Maintainer')
        data['maintainer_email'] = mdata.get('Maintainer-email')
        data['install_requires'] = mdata.get_all('Requires-Dist')

    return data


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class CaselessDict(Mapping[K, V]):
    """A dictionary with case-insensitive string getters."""

    def __init__(self, *args: Union[Mapping[K, V], Collection[Tuple[K, V]]], **kwargs: Mapping[K, V]) -> None:
        self._map: Dict[K, V] = dict(*args, **kwargs)
        self._caseless: Dict[str, str] = {k.lower(): k for k, v in self._map.items() if isinstance(k, str)}
        self._hash: int = -1

    def __contains__(self, key: object) -> bool:
        """Test if <key> is contained within this mapping."""
        return (
            self._caseless[key.lower()] in self._map
            if (isinstance(key, str) and key.lower() in self._caseless)
            else key in self._map
        )

    def __copy__(self) -> "CaselessDict":
        """Return a shallow copy of this mapping."""
        return type(self)(self.items())

    def __eq__(self, other: Any) -> bool:
        """Test if <other> is equal to this class instance."""
        ret = isinstance(other, type(self))
        ret = ret and hasattr(other, "__hash__")
        ret = ret and hash(self) == hash(other)
        ret = ret and hasattr(other, "__len__")
        ret = ret and len(self) == len(other)
        ret = ret and all([key in other and other[key] == value for key, value in self.items()])
        return ret

    def __getitem__(self, key: K) -> Any:
        """Return a value indexed with <key>."""
        if isinstance(key, str) and key.lower() in self._caseless:
            return self._map[cast(K, self._caseless[key.lower()])]
        else:
            return self._map[key]

    def __hash__(self) -> int:
        """Return a hash of this dictionary using all key-value pairs."""
        if self._hash == -1 and self:
            current: int = 0
            for key, value in self.items():
                if isinstance(key, str):
                    current ^= hash((key.lower(), value))
                else:
                    current ^= hash((key, value))
            current ^= maxsize
            self._hash = current
        return self._hash

    def __iter__(self) -> Iterator[K]:
        """Return an iterator over the keys."""
        return iter(self._map.keys())

    def __len__(self) -> int:
        """Return the length of the mapping."""
        return len(self._map)

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __nonzero__(self) -> bool:
        """Test if this mapping is of non-zero length."""
        return bool(self._map)

    def __reduce__(self) -> Tuple[Type["CaselessDict"], Tuple[List[Tuple[K, V]]]]:
        """Return a recipe for pickling."""
        return type(self), (list(self.items()),)

    def __repr__(self) -> str:
        """Return a representation of this class instance."""
        return f"{self.__class__.__qualname__}({repr(self._map)})"

    def __sizeof__(self) -> int:
        """Return the size of this class instance."""
        return getsizeof(self._map)

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return self.__repr__()

    @classmethod
    def fromkeys(cls, keys: Collection[K], default: V) -> "CaselessDict":
        """Build a mapping from a set of keys with a default value."""
        return cls([(key, default) for key in keys])

    def copy(self, mapping: Optional[Dict[K, V]] = None) -> "CaselessDict":
        """Return a shallow copy of this mapping."""
        overrides: Dict[K, V] = {}
        if mapping is not None:
            for k, v in mapping.items():
                if isinstance(k, str) and k.lower() in self._caseless:
                    overrides[cast(K, self._caseless[k.lower()])] = v
                else:
                    overrides[k] = v
        return type(self)((list(self.items())) + list(overrides.items()))

    def get(self, key: K, default: Optional[Any] = None) -> Union[Any, V]:
        """Return a value indexed with <key> but if that key is not present, return <default>."""
        if isinstance(key, str) and key.lower() in self._caseless:
            caseless_key: K = cast(K, self._caseless[key.lower()])
            return self._map.get(caseless_key, default)
        else:
            return self._map.get(key, default)

    def items(self) -> ItemsView[K, V]:
        """Return this mapping as a list of paired key-values."""
        return self._map.items()

    def keys(self) -> KeysView[K]:
        """Return the keys in insertion order."""
        return self._map.keys()

    def updated(self, key: K, value: V) -> "CaselessDict":
        """Return a shallow copy of this mapping with a key-value pair."""
        return self.copy({key: value})

    def values(self) -> ValuesView[V]:
        """Return the values in insertion order."""
        return self._map.values()


def pypi_text_file(pkg_info_path):
    pkg_info_file = open(pkg_info_path, 'r')
    text = pypi_text_stream(pkg_info_file)
    pkg_info_file.close()
    return text


def pypi_text_stream(pkg_info_stream):
    pkg_info_lines = parser.Parser().parse(pkg_info_stream)
    return pypi_text_items(pkg_info_lines.items())


def pypi_text_metaextract(library):
    pkg_info_lines = metadata.metadata(library)
    return pypi_text_items(pkg_info_lines.items())


def pypi_text_items(pkg_info_items):
    pkg_info_dict = {}
    for key, value in pkg_info_items:
        key = key.lower().replace('-', '_')
        if key in {'requires_dist', 'provides_extra'}:
            val = dict.setdefault(pkg_info_dict, key, [])
            val.append(value)
        elif key in {'classifier'}:
            val = dict.setdefault(pkg_info_dict, key + 's', [])
            val.append(value)
        elif key in {'project_url'}:
            key1, val = value.split(',', 1)
            pkg_info_dict.setdefault(key + 's', {})[key1.strip()] = val.strip()
        else:
            pkg_info_dict[key] = value
    return {'info': pkg_info_dict, 'urls': []}


def pypi_json_file(file_path):
    json_file = open(file_path, 'r')
    js = pypi_json_stream(json_file)
    json_file.close()
    return js


def pypi_json_stream(json_stream):
    js = json.load(json_stream)
    if 'info' not in js:
        js = {'info': js}
    if 'urls' not in js:
        js['urls'] = []
    return js


def _check_if_pypi_archive_file(path):
    return path.count('/') == 1 and os.path.basename(path) == 'PKG-INFO'


def pypi_archive_file(file_path):
    if tarfile.is_tarfile(file_path):
        with tarfile.open(file_path, 'r') as archive:
            for member in archive.getmembers():
                if _check_if_pypi_archive_file(member.name):
                    return pypi_text_stream(StringIO(archive.extractfile(member).read().decode()))
    elif zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as archive:
            for member in archive.namelist():
                if _check_if_pypi_archive_file(member):
                    return pypi_text_stream(StringIO(archive.open(member).read().decode()))
    else:
        raise TypeError("Can not extract '%s'. Not a tar or zip file" % file_path)
    raise KeyError('PKG-INFO not found on archive ' + file_path)


def parse_vars(items):
    """
        Parse a series of key-value pairs and return a dictionary and
        a success boolean for whether each item was successfully parsed.
    """
    if not items:
        return {}

    d = {}
    for item in items:
        index = item.find('=')
        if index > 0:
            split_string = (item[:index], item[(index + 1):])
            d[split_string[0]] = split_string[1]
        else:
            d[item] = True

    return d
