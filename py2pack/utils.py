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

from contextlib import contextmanager
import os
import shutil
import tarfile
import tempfile
import zipfile
from six.moves import filter


@contextmanager
def _extract_to_tempdir(filename):
    """extract the given filename to a tempdir and change the cwd to the
    new tempdir"""
    tempdir = tempfile.mkdtemp(prefix="py2pack_")
    current_cwd = os.getcwd()
    names = []
    try:
        if tarfile.is_tarfile(filename):
            with tarfile.open(filename) as f:
                names = f.getnames()
                f.extractall(tempdir)
        elif zipfile.is_zipfile(filename):
            with zipfile.ZipFile(filename) as f:
                names = f.namelist()
                f.extractall(tempdir)
        else:
            raise Exception("Can not extract '%s'. Not a tar or zip file" % filename)
        os.chdir(tempdir)
        yield tempdir, filter(lambda x: x != './', names)
    finally:
        os.chdir(current_cwd)
        shutil.rmtree(tempdir)
