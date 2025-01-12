%define pypi_name py2pack
%define python_name python3-%{pypi_name}
Name:           python-%{pypi_name}
Version:        0.8.5
Release:        %autorelease
Summary:        Generate distribution packages from PyPI

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        Apache-2.0
URL:            http://github.com/openSUSE/py2pack
Source:         

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python-devel
BuildRequires:  fdupes
BuildArch:      noarch

# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
Py2pack: Generate distribution packages from PyPI
=================================================

.. image:: https://travis-ci.org/openSUSE/py2pack.png?branch=master
        :target: https://travis-ci.org/openSUSE/py2pack


This script allows to generate RPM spec or DEB dsc files from Python modules.
It allows to list Python modules or search for them on the Python Package Index
(PyPI). Conveniently, it can fetch tarballs and changelogs making it an
universal tool to package Python modules.


Installation
------------

To install py2pack from the `Python Package Index`_, simply:

.. code-block:: bash

    $ pip install py2pack

Or, if you absolutely must:

.. code-block:: bash

    $ easy_install py2pack

But, you really shouldn't do that. Lastly, you can check your distro of choice
if they provide packages. For openSUSE, you can find packages in the `Open
Build Service`_ for all releases. If you happen to use openSUSE:Factory (the
rolling release / development version), simply:

.. code-block:: bash

    $ sudo zypper install python-py2pack


Usage
-----

Lets suppose you want to package zope.interface_ and you don't know how it is named
exactly. First of all, you can search for it and download the source tarball if
you found the correct module:

.. code-block:: bash

    $ py2pack search zope.interface
    searching for module zope.interface...
    found zope.interface-3.6.1
    $ py2pack fetch zope.interface
    downloading package zope.interface-3.6.1...
    from http://pypi.python.org/packages/source/z/zope.interface/zope.interface-3.6.1.tar.gz


As a next step you may want to generate a package recipe for your distribution.
For RPM_-based distributions (let's use openSUSE_ as an example), you want to
generate a spec file (named 'python-zope.interface.spec'):

.. code-block:: bash

    $ py2pack generate zope.interface -t opensuse.spec -f python-zope.interface.spec

The source tarball and the package recipe is all you need to generate the RPM_
(or DEB_) file.
This final step may depend on which distribution you use. Again,
for openSUSE_ (and by using the `Open Build Service`_), the complete recipe is:

.. code-block:: bash

    $ osc mkpac python-zope.interface
    $ cd python-zope.interface
    $ py2pack fetch zope.interface
    $ py2pack generate zope.interface -f python-zope.interface.spec
    $ osc build
    ...

Depending on the module, you may have to adapt the resulting spec file slightly.
To get further help about py2pack usage, issue the following command:

.. code-block:: bash

    $ py2pack help


Hacking and contributing
------------------------

You can test py2pack from your git checkout by executing the py2pack module:

.. code-block:: bash

    $ python -m py2pack

Fork `the repository`_ on Github to start making your changes to the **master**
branch (or branch off of it). Don't forget to write a test for fixed issues or
implemented features whenever appropriate. You can invoke the testsuite from
the repository root directory via `tox`_:

.. code-block:: bash

    $ tox

To run a single test class via `tox`_, use i.e.:

.. code-block:: bash

    $ tox -epy27 test.test_py2pack:Py2packTestCase


You can also run `pytest`_ directly:

.. code-block:: bash

    $ pytest

It assumes you have the test dependencies installed (available on PYTHONPATH)
on your system.

:copyright: (c) 2013 Sascha Peilicke.
:license: Apache-2.0, see LICENSE for more details.


.. _argparse: http://pypi.python.org/pypi/argparse
.. _Jinja2: http://pypi.python.org/pypi/Jinja2
.. _zope.interface: http://pypi.python.org/pypi/zope.interface/
.. _openSUSE: http://www.opensuse.org/en/
.. _RPM: http://en.wikipedia.org/wiki/RPM_Package_Manager
.. _DEB: http://en.wikipedia.org/wiki/Deb_(file_format)
.. _`Python Package Index`: https://pypi.org/
.. _`Open Build Service`: https://build.opensuse.org/package/show/devel:languages:python/python-py2pack
.. _`the repository`: https://github.com/openSUSE/py2pack
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: http://testrun.org/tox}

%description %_description

%package -n %{python_name}
Summary:        %{summary}


%description -n %{python_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%generate_buildrequires
%pyproject_buildrequires 


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto
%if %{with test}
%check
%pyproject_check_import
%pytest
%endif


%files -n %{python_name} -f %{pyproject_files}


%changelog
%autochangelog

