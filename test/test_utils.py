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

    def test__get_archive_filelist_invalid_archive(self):
        file_name = os.path.join(self.tmpdir, "file.txt")
        # poor man's touch
        with open(file_name, "w") as txt_file:
            txt_file.write('')

        with self.assertRaises(ValueError) as val_err:
            py2pack.utils._get_archive_filelist(file_name)

        self.assertIn(file_name, str(val_err.exception))
        self.assertIn("Not a tar or zip file", str(val_err.exception))

    def test__get_archive_filelist_nonexistent_file(self):
        file_name = os.path.join(
            self.tmpdir, "this_does_not_exist.asdfqweruiae")

        # tarfile.is_tarfile() throws an IOError in Python2.7 and
        # FileNotFoundError  in Python3.6
        try:
            expected_err = eval('FileNotFoundError')
        except NameError:
            expected_err = IOError

        with self.assertRaises(expected_err) as f_not_found_err:
            py2pack.utils._get_archive_filelist(file_name)

        self.assertNotIn(
            "Not a tar or zip file", str(f_not_found_err.exception))
