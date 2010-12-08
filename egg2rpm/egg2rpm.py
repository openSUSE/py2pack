#!/usr/bin/python
#
# Copyright (c) 2010, Sascha Peilicke <saschpe@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (see the file COPYING); if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import argparse, os, urllib, xmlrpclib

pypi = xmlrpclib.ServerProxy('http://python.org/pypi')

def list(args):
    print('listing all PyPI packages...')
    for package in pypi.list_packages():
        print(package)

def search(args):
    print('searching for {0}...'.format(args.name))
    for hit in pypi.search({'name': args.name}):
        print('found {0}-{1}'.format(hit['name'], hit['version']))

def fetch(args):
    if not args.version:
        args.version = pypi.search({'name': args.name})[0]['version']
    print('downloading {0}-{1}...'.format(args.name, args.version))
    for url in pypi.package_urls(args.name, args.version):          # fetch all download URLs
        if url['packagetype'] == 'sdist':                           # found the source URL we care for
            print('from {0}'.format(url['url']))
            urllib.urlretrieve(url['url'], url['filename'])         # download the object behind the URL

def build(args):
    print('build {0}'.format(args.url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--version', action='version', version='%(prog)s TODO')
    subparsers = parser.add_subparsers(title='commands')

    parser_list = subparsers.add_parser('list', help='list all packages on PyPI')
    parser_list.set_defaults(func=list)

    parser_search = subparsers.add_parser('search', help='search for packages on PyPI')
    parser_search.add_argument('name', type=str, help='package name')
    parser_search.set_defaults(func=search)

    parser_fetch = subparsers.add_parser('fetch', help='download a package from PyPI')
    parser_fetch.add_argument('name', type=str, help='package name')
    parser_fetch.add_argument('version', type=str, nargs='?', help='package version (optional)')
    parser_fetch.set_defaults(func=fetch)

    args = parser.parse_args()
    args.func(args)

