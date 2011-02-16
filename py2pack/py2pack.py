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

import argparse, os, pwd, sys, urllib, xmlrpclib
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates') # absolute template path

pypi = xmlrpclib.ServerProxy('http://python.org/pypi')                      # XML RPC connection to PyPI
env = Environment(loader = FileSystemLoader(TEMPLATE_DIR))                  # Jinja2 template environment


def list(args):
    print('listing all PyPI packages...')
    for package in pypi.list_packages():                                    # nothing fancy
        print(package)

def search(args):
    print('searching for package {0}...'.format(args.name))
    for hit in pypi.search({'name': args.name}):
        print('found {0}-{1}'.format(hit['name'], hit['version']))

def show(args):
    check_or_set_version(args)
    print('showing package {0}...'.format(args.name))
    data = pypi.release_data(args.name, args.version)                       # fetch all meta data
    pprint(data)

def fetch(args):
    check_or_set_version(args)
    url = newest_download_url(args)
    if not url:
      print("unable to find a source release for {0}!".format(args.name))   # pass out if nothing is found
      sys.exit(1)
    print('downloading package {0}-{1}...'.format(args.name, args.version))
    print('from {0}'.format(url['url']))
    urllib.urlretrieve(url['url'], url['filename'])                         # download the object behind the URL

def generate(args):
    check_or_set_version(args)
    if not args.template:
        args.template = template_list()[0]
    if not args.filename:
        args.filename = args.name + '.' + args.template.rsplit('.', 1)[1]   # take template file ending
    print('generating spec file for {0}...'.format(args.name))
    data = pypi.release_data(args.name, args.version)                       # fetch all meta data
    url = newest_download_url(args)
    if url:
      data['ending'] = url['filename'].rsplit(args.name + "-" + args.version)[1] # split of name-version to get ending
    else:
      data['ending'] = '.zip'                                               # set sane default if no download available
    data['year'] = datetime.now().year                                      # set current year
    data['user_name'] = pwd.getpwuid(os.getuid())[4]                        # set system user (packager)
    template = env.get_template(args.template)
    result = template.render(data)
    outfile = open(args.filename, 'w')                                      # write result to spec file
    try:
        outfile.write(result)
    finally:
        outfile.close()

def check_or_set_version(args):
    if not args.version:                                                    # take first version found
        releases = pypi.package_releases(args.name)
        if len(releases) == 0:
            print("unable to find a suitable release for {0}!".format(args.name))
            sys.exit(1)
        else:
            args.version = pypi.package_releases(args.name)[0]              # return first (current) release number

def newest_download_url(args):
    for url in pypi.package_urls(args.name, args.version):                  # fetch all download URLs
        if url['packagetype'] == 'sdist':                                   # found the source URL we care for
            return url
    return []

def template_list():
    return os.listdir(TEMPLATE_DIR)


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    subparsers = parser.add_subparsers(title='commands')

    parser_list = subparsers.add_parser('list', help='list all packages on PyPI')
    parser_list.set_defaults(func=list)

    parser_search = subparsers.add_parser('search', help='search for packages on PyPI')
    parser_search.add_argument('name', help='package name (with optional version)')
    parser_search.set_defaults(func=search)

    parser_show = subparsers.add_parser('show', help='show metadata for package')
    parser_show.add_argument('name', help='package name')
    parser_show.add_argument('version', nargs='?', help='package version (optional)')
    parser_show.set_defaults(func=show)

    parser_fetch = subparsers.add_parser('fetch', help='download package source tarball from PyPI')
    parser_fetch.add_argument('name', help='package name')
    parser_fetch.add_argument('version', nargs='?', help='package version (optional)')
    parser_fetch.set_defaults(func=fetch)

    parser_spec = subparsers.add_parser('generate', help='generate RPM spec or DEB dsc file for a package')
    parser_spec.add_argument('name', help='package name')
    parser_spec.add_argument('version', nargs='?', help='package version (optional)')
    parser_spec.add_argument('-t', '--template', choices=template_list(), help='spec file template')
    parser_spec.add_argument('-f', '--filename', help='spec filename (optional)')
    parser_spec.set_defaults(func=generate)

    parser_help = subparsers.add_parser('help', help='show this help')
    parser_help.set_defaults(func=lambda args: parser.print_help())

    args = parser.parse_args()
    args.func(args)


# fallback if run directly
if __name__ == '__main__':
    main()
