# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Thomas Bechtold <tbechtold@suse.com>
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

import os
import shutil
import tarfile
import tempfile
import unittest

import py2pack.utils


class Py2packUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='py2pack_test_')

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _create_tarfile(self, name="file.tar"):
        tarfile_name = os.path.join(self.tmpdir, name)
        tar = tarfile.open(tarfile_name, "w:gz")
        for name in ["file1", "file2", "file3"]:
            new_file = os.path.join(self.tmpdir, name)
            with open(new_file, "a+") as f:
                f.write(name)
            tar.add(new_file, arcname=name)
        tar.close()
        return tarfile_name

    def _create_zipfile(self, name="file"):
        zipfile_name = os.path.join(self.tmpdir, name)
        zip_data = os.path.join(self.tmpdir, "data")
        os.mkdir(zip_data)
        for name in ["file1", "file2", "file3"]:
            new_file = os.path.join(zip_data, name)
            with open(new_file, "a+") as f:
                f.write(name)
        shutil.make_archive(zipfile_name, "zip", root_dir=zip_data)
        return zipfile_name + ".zip"

    def test__get_archive_filelist_tarfile(self):
        file_name = self._create_tarfile()
        expected_files = sorted(["file1", "file2", "file3"])
        files = py2pack.utils._get_archive_filelist(file_name)
        self.assertEqual(expected_files, files)

    def test__get_archive_filelist_zipfile(self):
        file_name = self._create_zipfile()
        expected_files = sorted(["file1", "file2", "file3"])
        files = py2pack.utils._get_archive_filelist(file_name)
        self.assertEqual(expected_files, files)
