=======
py2pack
=======

This script allows to generate RPM spec or DEB dsc files from Python modules.
It allows to list Python modules or search for them on the Python Package Index
(PyPI). Conveniently, it can fetch tarballs and changelogs making it an
universal tool to package Python modules.


Prerequisites
=============

py2pack needs the argparse_ Python module installed. It is also part of
the Python-2.7 Standard Library. Additionally, it uses the Jinja2_ templating
engine.


Usage
=====

Lets suppose you want to package zope.interface_ and you don't know how it is named
exactly. First of all, you can search for it and download the source tarball if
you found the correct module::

 $ py2pack search zope.interface
 searching for module zope.interface...
 found zope.interface-3.6.1
 $ py2pack fetch zope.interface
 downloading package zope.interface-3.6.1...
 from http://pypi.python.org/packages/source/z/zope.interface/zope.interface-3.6.1.tar.gz

As a next step you may want to generate a package recipe for your distribution.
For RPM_-based distributions (let's use openSUSE_ as an example), you want to
generate a spec file (named 'python-zope.interface.spec')::

 $ py2pack generate zope.interface -t opensuse.spec -f python-zope.interface.spec

The source tarball and the package recipe is all you need to generate the RPM_
(or DEB_) file. This final step may depend on which distribution you use. Again,
for openSUSE_ (and by using the `openSUSE Build Service`_), the complete recipe is::

 $ osc mkpac python-zope.interface
 $ cd python-zope.interface
 $ py2pack fetch zope.interface
 $ py2pack generate zope.interface -f python-zope.interface.spec
 $ osc build
 ...

Depending on the module, you may have to adapt the resulting spec file slightly.
To get further help about py2pack usage, issue the following command::

 $ py2pack help


License
=======

See the file LICENSE.

.. _argparse: http://pypi.python.org/pypi/argparse
.. _Jinja2: http://pypi.python.org/pypi/Jinja2 
.. _zope.interface: http://pypi.python.org/pypi/zope.interface/
.. _openSUSE: http://www.opensuse.org/en/
.. _openSUSE Build Service: https://build.opensuse.org/
.. _RPM: http://en.wikipedia.org/wiki/RPM_Package_Manager
.. _DEB: http://en.wikipedia.org/wiki/Deb_(file_format)
