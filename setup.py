#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os,subprocess, sys
import py2pack


if sys.argv[-1] == "doc":
    """Generate manpage, HTML and PDF documentation.
    """
    try:
        subprocess.call(["xsltproc", "--output", "doc/py2pack.html", "/usr/share/xml/docbook/stylesheet/nwalsh/current/html/docbook.xsl", "doc/py2pack.xml.in"])
        subprocess.call(["xsltproc", "--output", "doc/py2pack.1", "/usr/share/xml/docbook/stylesheet/nwalsh/current/manpages/docbook.xsl", "doc/py2pack.xml.in"])
        #subprocess.call(["xsltproc", "--output", "doc/py2pack.fo",
        #                 "--stringparam", "paper.type", "A4",
        #                 "--stringparam", "body.start.indent", "0pt",
        #                 "--stringparam", "title.margin.left", "0pt",
        #                 "--stringparam", "variablelist.as.blocks", "1",
        #                 "/usr/share/xml/docbook/stylesheet/nwalsh/current/fo/docbook.xsl", "doc/py2pack.xml.in"])
        #subprocess.call(["fop", "doc/py2pack.fo", "doc/py2pack.pdf"])
    except:
        pass
    #if os.path.exists("doc/py2pack.fo"):
    #    os.remove("doc/py2pack.fo")
    sys.exit()

setup(
    name = py2pack.__name__,
    version = py2pack.__version__,
    license = "GPLv2",
    description = py2pack.__doc__,
    long_description = open('README.rst').read(),
    author = py2pack.__author__.rsplit(' ', 1)[0],
    author_email = py2pack.__author__.rsplit(' ', 1)[1][1:-1],
    url = 'http://github.com/saschpe/py2pack',
    scripts = ['scripts/py2pack'],
    packages = ['py2pack'],
    package_data = {'py2pack': ['templates/*']},
    data_files = [('share/doc/py2pack', ['AUTHORS', 'LICENSE', 'README.rst']),
                  ('share/doc/py2pack/html', ['doc/py2pack.html']),
                  #('share/doc/py2pack/pdf', ['doc/py2pack.pdf']),
                  ('man/man1', ['doc/py2pack.1'])],
    requires = ['argparse', 'Jinja2'],
    classifiers = [
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
