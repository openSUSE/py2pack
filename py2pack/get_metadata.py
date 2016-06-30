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


# The file contains a distutils command to print metadata to the console
# or write it to a file.


from distutils.core import Command
import json


class get_metadata(Command):
    """a distutils command to get metadata"""
    description = "get package metadata"
    user_options = [
        ("output=", "o", "output for metadata json")
    ]

    def initialize_options(self):
        self.output = None

    def finalize_options(self):
        pass

    def run(self):
        data = {}
        if self.distribution.has_ext_modules():
            data["is_extension"] = True
        if getattr(self.distribution, "scripts", None):
            data["scripts"] = self.distribution.scripts
        if getattr(self.distribution, "test_suite", None):
            data["test_suite"] = self.distribution.test_suite
        if getattr(self.distribution, "install_requires", None):
            data["install_requires"] = self.distribution.install_requires
        if getattr(self.distribution, "extras_require", None):
            data["extras_require"] = self.distribution.extras_require
        if getattr(self.distribution, "tests_require", None):
            data["tests_require"] = self.distribution.tests_require
        if getattr(self.distribution, "data_files", None):
            data["data_files"] = self.distribution.data_files
        if getattr(self.distribution, "entry_points", None):
            data["entry_points"] = self.distribution.entry_points

        if self.output:
            with open(self.output, "w+") as f:
                f.write(json.dumps(data, indent=2))
        else:
            print(json.dumps(data, indent=2))
