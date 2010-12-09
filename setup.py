from distutils.core import setup
import py2pack

f = open('README')
try:
    README = f.read()
finally:
    f.close()

setup(
    name = py2pack.__name__,
    version = py2pack.__version__,
    license = "GPLv2",
    description = py2pack.__doc__,
    long_description = README,
    author = py2pack.__author__.split(' ')[0],
    author_email = py2pack.__author__.split(' ')[1],
    url = 'http://github.com/saschpe/py2pack',
    scripts = ['py2pack'],
    install_requires = ['argparse', 'Jinja2']
)
