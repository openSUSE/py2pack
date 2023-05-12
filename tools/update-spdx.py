#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Sascha Peilicke <sascha@peilicke.de>
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

import json

import lxml.html
import requests


LICENSE_FILE = 'py2pack/spdx_license_map.json'


def update_spdx():
    """Update SDPX license map."""
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
    json.dump(licenses, open(LICENSE_FILE, 'w'), indent=2)


if __name__ == "__main__":
    update_spdx()
