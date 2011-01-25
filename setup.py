from distutils.core import setup
import py2pack

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
    #data_files = [('doc/py2pack', ['AUTHORS', 'LICENSE', 'README'])],
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
