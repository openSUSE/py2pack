#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013, Sascha Peilicke <saschpe@gmx.de>
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

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import py2pack
import py2pack.setup


install_requires = py2pack.setup.parse_requirements("requirements.txt")
tests_requires = py2pack.setup.parse_requirements("test-requirements.txt")

with open("README.rst", "r") as f:
    long_description = f.read()


setup(
    name=py2pack.__name__,
    version=py2pack.__version__,
    license="GPLv2",
    description=py2pack.__doc__,
    long_description=long_description,
    author=py2pack.__author__.rsplit(' ', 1)[0],
    author_email=py2pack.__author__.rsplit(' ', 1)[1][1:-1],
    url='http://github.com/saschpe/py2pack',
    scripts=['scripts/py2pack'],
    packages=['py2pack'],
    package_data={'py2pack': ['templates/*', 'suse_spdx_license_map.p']},
    data_files=[('share/doc/py2pack', ['AUTHORS', 'LICENSE', 'README.rst']),
                ('share/doc/py2pack/html', ['doc/py2pack.html']),
                #('share/doc/py2pack/pdf', ['doc/py2pack.pdf']),
                ('man/man1', ['doc/py2pack.1'])],
    setup_requires=["lxml", "requests"],
    install_requires=install_requires,
    cmdclass=py2pack.setup.get_cmdclass(),
    tests_require=tests_requires,
    test_suite="nose.collector",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Pre-processors',
    ],
)
