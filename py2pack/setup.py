# Copyright 2013 Sascha Peilicke
# Copyright 2016 Thomas Bechtold
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import subprocess
from distutils.core import Command

from py2pack.get_metadata import get_metadata


class DocCommand(Command):
    description = "Generate manpage, HTML and PDF documentation"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            subprocess.call(["xsltproc", "--output", "doc/py2pack.html", "/usr/share/xml/docbook/stylesheet/nwalsh/current/html/docbook.xsl", "doc/src/py2pack.xml.in"])
            subprocess.call(["xsltproc", "--output", "doc/py2pack.1", "/usr/share/xml/docbook/stylesheet/nwalsh/current/manpages/docbook.xsl", "doc/src/py2pack.xml.in"])
        except:
            pass


class SPDXUpdateCommand(Command):
    description = "Update SDPX license map"
    user_options = []
    LICENSE_FILE = 'py2pack/spdx_license_map.p'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Not part of any requirements, could happen through setup(setup_requires=...)
        import pickle
        import lxml.html
        import requests
        response = requests.get('https://docs.google.com/spreadsheet/pub?key=0AqPp4y2wyQsbdGQ1V3pRRDg5NEpGVWpubzdRZ0tjUWc')
        html = lxml.html.fromstring(response.text)
        licenses = {}
        for i, tr in enumerate(html.cssselect('table.waffle > tbody > tr')):
            _, td_new, td_old = tr.getchildren()
            licenses[td_old.text] = td_new.text
            # also add the spdx license as key (i.e. key/value "Apache-2.0"->"Apache-2.0")
            # Otherwise licenses for packages which already have a SPDX compatible license
            # are not correctly recognized
            licenses[td_new.text] = td_new.text
        pickle.dump(licenses, open(SPDXUpdateCommand.LICENSE_FILE, 'wb'))


def get_cmdclass():
    """Dictionary of all distutils commands defined in this module.
    """
    return {
        "spdx_update": SPDXUpdateCommand,
        "get_metadata": get_metadata,
    }


def parse_requirements(requirements_file='requirements.txt'):
    requirements = []
    with open(requirements_file, 'r') as f:
        for line in f:
            # For the requirements list, we need to inject only the portion
            # after egg= so that distutils knows the package it's looking for
            # such as:
            # -e git://github.com/openstack/nova/master#egg=nova
            if re.match(r'\s*-e\s+', line):
                requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1',
                                    line))
            # such as:
            # http://github.com/openstack/nova/zipball/master#egg=nova
            elif re.match(r'\s*https?:', line):
                requirements.append(re.sub(r'\s*https?:.*#egg=(.*)$', r'\1',
                                    line))
            # -f lines are for index locations, and don't get used here
            elif re.match(r'\s*-f\s+', line):
                pass
            # -r lines are for including other files, and don't get used here
            elif re.match(r'\s*-r\s+', line):
                pass
            else:
                requirements.append(line.strip())
    return requirements
