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

.. _Jinja2: http://jinja.pocoo.org/docs/dev/
