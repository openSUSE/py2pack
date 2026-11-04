Templates
---------

py2pack uses `Jinja2`_ based templates to generate RPM spec or DEB dsc files.
There are multiple directories used to search for templates:

  * ~/.py2pack/templates/
  * /usr/share/py2pack/templates/
  * prefix/lib/pythonX.Y/site-packages/py2pack/templates/ (included in py2pack)

Template files found in the first search path (~/.py2pack/templates/) win.
To get a list of available templates, do:

.. code-block:: bash

    $ py2pack generate -h

Fedora
~~~~~~

The Fedora template targets currently supported Fedora releases with Python 3
and the ``%pyproject_*`` RPM macros. It does not generate Python 2 packages or
provide compatibility with legacy Enterprise Linux releases.

It builds a wheel, generates build requirements from the build backend, and
puts runtime dependencies in the Python 3 subpackage. Declared build-system
requirements are also listed explicitly. When test metadata is available,
``%bcond_without test`` enables test dependencies and a ``%check`` section.
Review the generated test runner and arguments against upstream's instructions.
Use ``rpmbuild --without test`` to disable the tests and their dependencies.

Import names are read from the distribution's ``.egg-info/top_level.txt`` when
available. Otherwise, the template guesses a module name from the distribution
name and marks it for review. PyPI names and import names need not match.
Correct the arguments to ``%pyproject_save_files`` before building if necessary;
do not replace them with a blanket ``'*'`` glob or ``+auto``.

The file manifest handles Python modules and distribution metadata. Executables,
source documentation, licence files and known installed data files are listed
separately. Review ownership of package-specific data directories and add any
files that upstream's metadata did not describe. Legacy scripts keep their
basenames, and console entry points keep their normal executable names.

Fedora RPM build tests
^^^^^^^^^^^^^^^^^^^^^^

The Fedora CI job builds small example RPMs for legacy setuptools, PEP 517-only,
native-extension and executable-script projects. It also checks that disabling
tests works. These build tests are opt-in outside CI and require Fedora, GCC,
``rpm-build``, ``pyproject-rpm-macros``, ``python3-devel``, ``python3-setuptools``,
``python3-wheel`` and ``python3-pytest``, alongside py2pack's test dependencies.

.. code-block:: bash

    PY2PACK_TEST_FEDORA_BUILDS=1 python3 -m pytest -v test/test_fedora_build.py

The template regression tests in ``test/test_fedora_template.py`` run without
network access or RPM tools.

.. _Jinja2: http://jinja.pocoo.org/docs/dev/
