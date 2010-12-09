#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint

#TODO: Move into setup.py
TEMPLATE_DIR = 'templates'

pypi = xmlrpclib.ServerProxy('http://python.org/pypi')              # XML RPC connection to PyPI
env = Environment(loader = FileSystemLoader(TEMPLATE_DIR))          # Jinja2 template environment

def list(args):
    print('listing all PyPI modules...')
    for module in pypi.list_modules():
        print(module)

def search(args):
    print('searching for module {0}...'.format(args.name))
    for hit in pypi.search({'name': args.name}):
        print('found {0}-{1}'.format(hit['name'], hit['version']))

def show(args):
    if not args.version:                                            # take first version found
        args.version = pypi.search({'name': args.name})[0]['version']
    print('showing module {0}...'.format(args.name))
    data = pypi.release_data(args.name, args.version)               # fetch all meta data
    pprint(data)

def fetch(args):
    if not args.version:                                            # take first version found
        args.version = pypi.search({'name': args.name})[0]['version']
    print('downloading module {0}-{1}...'.format(args.name, args.version))
    for url in pypi.module_urls(args.name, args.version):          # fetch all download URLs
        if url['moduletype'] == 'sdist':                           # found the source URL we care for
            print('from {0}'.format(url['url']))
            urllib.urlretrieve(url['url'], url['filename'])         # download the object behind the URL

def gen_spec(args):
    if not args.version:                                            # take first version found
        args.version = pypi.search({'name': args.name})[0]['version']
    print('generating spec file for {0}...'.format(args.name))
    data = pypi.release_data(args.name, args.version)               # fetch all meta data
    template = env.get_template(args.template + '.spec.template')
    #TODO: Dependencies should be read from the tarball if meta doesn't provide them
    #TODO: Additional files for the %files section have to be fetched from the tarball
    result = template.render(data)
    with open(args.name + '.spec', 'w') as outfile:                 # write result to spec file
        outfile.write(result)

def gen_dsc(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Generate packages from Python modules on PyPI')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    subparsers = parser.add_subparsers(title='commands')

    parser_list = subparsers.add_parser('list', help='list all modules on PyPI')
    parser_list.set_defaults(func=list)

    parser_search = subparsers.add_parser('search', help='search for modules on PyPI')
    parser_search.add_argument('name', help='module name')
    parser_search.set_defaults(func=search)

    parser_show = subparsers.add_parser('show', help='show metadata for module')
    parser_show.add_argument('name', help='module name')
    parser_show.add_argument('version', nargs='?', help='module version (optional)')
    parser_show.set_defaults(func=show)

    parser_fetch = subparsers.add_parser('fetch', help='download module source tarball from PyPI')
    parser_fetch.add_argument('name', help='module name')
    parser_fetch.add_argument('version', nargs='?', help='module version (optional)')
    parser_fetch.set_defaults(func=fetch)

    parser_spec = subparsers.add_parser('genspec', help='generate RPM spec file for a module')
    parser_spec.add_argument('name', help='module name')
    parser_spec.add_argument('version', nargs='?', help='module version (optional)')
    parser_spec.add_argument('template', choices=['opensuse'], help='spec file template')
    parser_spec.set_defaults(func=gen_spec)

    parser_help = subparsers.add_parser('help', help='show this help')
    # TODO: allow to display module-specific help too
    parser_help.set_defaults(func=lambda args: parser.print_help())

    args = parser.parse_args()
    args.func(args)
