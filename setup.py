#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Sascha Peilicke <sascha@peilicke.de>
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
    license="Apache-2.0",
    description=py2pack.__doc__,
    long_description=long_description,
    author=py2pack.__author__.rsplit(' ', 1)[0],
    author_email=py2pack.__author__.rsplit(' ', 1)[1][1:-1],
    url='http://github.com/saschpe/py2pack',
    scripts=['scripts/py2pack'],
    packages=['py2pack'],
    package_data={'py2pack': ['templates/*', 'spdx_license_map.p']},
    data_files=[('share/doc/py2pack', ['AUTHORS', 'LICENSE', 'README.rst']),
                ('share/doc/py2pack/html', ['doc/py2pack.html']),
                # ('share/doc/py2pack/pdf', ['doc/py2pack.pdf']),
                ('man/man1', ['doc/py2pack.1'])],
    setup_requires=["cssselect", "lxml", "requests"],
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
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Pre-processors',
    ],
)
