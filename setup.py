from distutils.core import setup

f = open('README')
try:
    README = f.read()
finally:
    f.close()

setup(
    name = 'egg2rpm',
    version = '0.1',
    license = "GPLv2",
    description = 'Generate packages from Python modules on PyPI'
    long_description = README,
    author = 'Sascha Peilicke',
    author_email = 'saschpe@gmx.de',
    url = 'http://github.com/saschpe/egg2rpm',
    scripts = ['egg2rpm'],
    install_requires = ['argparse']
)
