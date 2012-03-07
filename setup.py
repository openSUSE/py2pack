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

import os
import subprocess
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import py2pack


if sys.argv[-1] == "doc":
    """Generate manpage, HTML and PDF documentation.
    """
    try:
        subprocess.call(["xsltproc", "--output", "docs/py2pack.html", "/usr/share/xml/docbook/stylesheet/nwalsh/current/html/docbook.xsl", "docs/src/py2pack.xml.in"])
        subprocess.call(["xsltproc", "--output", "docs/py2pack.1", "/usr/share/xml/docbook/stylesheet/nwalsh/current/manpages/docbook.xsl", "docs/src/py2pack.xml.in"])
        #subprocess.call(["xsltproc", "--output", "doc/py2pack.fo",
        #                 "--stringparam", "paper.type", "A4",
        #                 "--stringparam", "body.start.indent", "0pt",
        #                 "--stringparam", "title.margin.left", "0pt",
        #                 "--stringparam", "variablelist.as.blocks", "1",
        #                 "/usr/share/xml/docbook/stylesheet/nwalsh/current/fo/docbook.xsl", "docs/py2pack.xml.in"])
        #subprocess.call(["fop", "docs/py2pack.fo", "docs/py2pack.pdf"])
    except:
        pass
    #if os.path.exists("docs/py2pack.fo"):
    #    os.remove("docs/py2pack.fo")
    sys.exit()

setup(
    name=py2pack.__name__,
    version=py2pack.__version__,
    license="GPLv2",
    description=py2pack.__doc__,
    long_description=open('README.rst').read(),
    author=py2pack.__author__.rsplit(' ', 1)[0],
    author_email=py2pack.__author__.rsplit(' ', 1)[1][1:-1],
    url='http://github.com/saschpe/py2pack',
    scripts=['scripts/py2pack'],
    packages=['py2pack'],
    package_data={'py2pack': ['templates/*']},
    data_files=[('share/doc/py2pack', ['AUTHORS', 'LICENSE', 'README.rst']),
                ('share/doc/py2pack/html', ['docs/py2pack.html']),
               #('share/doc/py2pack/pdf', ['docs/py2pack.pdf']),
                ('man/man1', ['doc/py2pack.1'])],
    requires=['argparse', 'Jinja2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Pre-processors',
    ],
)
