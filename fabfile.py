# -*- coding: utf-8 -*-

import lxml.html
import pickle
import pprint 
import requests


SPDX_LICENSE_FILE = 'py2pack/suse_spdx_license_map.p'


def dump_spdx_licenses():
    response = requests.get('https://docs.google.com/spreadsheet/pub?key=0AqPp4y2wyQsbdGQ1V3pRRDg5NEpGVWpubzdRZ0tjUWc') 
    html = lxml.html.fromstring(response.text)
    licenses = {}
    for i, tr in enumerate(html.cssselect('table#tblMain > tr[class!="rShim"]')):
        if i == 0: continue # Skip the first tr, only contains row descriptions
        _, td_new, td_old = tr.getchildren()
        licenses[td_old.text] = td_new.text
    pickle.dump(licenses, open(SPDX_LICENSE_FILE, 'wb'))


def print_spdx_licenses():
    pprint.pprint(pickle.load(open(SPDX_LICENSE_FILE, 'rb')))
