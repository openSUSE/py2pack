# Copyright (c) 2013, Sascha Peilicke <sascha@peilicke.de>
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

import argparse
import platformdirs
import datetime
import glob
import json
import os
import pprint
import pwd
import re
import sys
import warnings

import jinja2
import pypi_search.search
import requests
from metaextract import utils as meta_utils

import py2pack.requires
from py2pack import version as py2pack_version
from py2pack.utils import (_get_archive_filelist, get_pyproject_table,
                           parse_pyproject, get_setuptools_scripts,
                           get_metadata)
import io
from email import parser
try:
    import libarchive
except ModuleNotFoundError:
    libarchive = None

DEFAULT_TEMPLATE = 'opensuse.spec'
try:
    import distro
    DEFAULT_TEMPLATE = {
        'fedora': 'fedora.spec',
        'debian': 'opensuse.dsc',
        'mageia': 'mageia.spec'
    }.get(distro.id(), DEFAULT_TEMPLATE)
except ModuleNotFoundError:
    pass


def replace_string(output_string, replaces):
    for name, replacement in replaces.items():
        pattern = r'(?<!%)%{' + name + '}'  # Negative lookbehind to exclude "%%{name}"
        output_string = re.sub(pattern, replacement.replace(r'%', r'%%'), output_string)
    return output_string.replace(r'%%', r'%')


warnings.simplefilter('always', DeprecationWarning)


SPDX_LICENSES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spdx_license_map.json')
with open(SPDX_LICENSES_FILE, 'r') as fp:
    SPDX_LICENSES = json.load(fp)


def pypi_json(project, release=None):
    """Access the PyPI JSON API

    https://warehouse.pypa.io/api-reference/json.html
    """
    version = ('/' + release) if release else ''
    with requests.get('https://pypi.org/pypi/{}{}/json'.format(project, version)) as r:
        pypimeta = r.json()
    return pypimeta


def pypi_text_file(pkg_info_path):
    with open(pkg_info_path, 'r') as pkg_info_file:
        return pypi_text_stream(pkg_info_file)


def pypi_text_stream(pkg_info_stream):
    pkg_info_lines = parser.Parser().parse(pkg_info_stream)
    pkg_info_dict = {}
    for key, value in pkg_info_lines.items():
        key = key.lower().replace('-', '_')
        if key in {'classifiers', 'requires_dist', 'provides_extra'}:
            val = pkg_info_dict.get(key)
            if val is None:
                val = []
                pkg_info_dict[key] = val
            val.append(value)
        else:
            pkg_info_dict[key] = value
    return {'info': pkg_info_dict, 'urls': []}


def pypi_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return pypi_json_stream(json_file)


def pypi_json_stream(json_stream):
    js = json.load(json_stream)
    if 'info' not in js:
        js = {'info': js}
    if 'urls' not in js:
        js['urls'] = []
    return js


def pypi_archive_file(file_path):
    if libarchive is None:
        return None
    try:
        with libarchive.file_reader(file_path) as archive:
            for entry in archive:
                # Check if the entry's pathname matches the target filename
                if entry.pathname == 'PKG-INFO':
                    return pypi_text_stream(io.StringIO(entry.read().decode()))
            else:
                return None
    except Exception:
        return None


def _get_template_dirs():
    """existing directories where to search for jinja2 templates. The order
    is important. The first found template from the first found dir wins!"""
    return filter(lambda x: os.path.exists(x), [
        os.path.join(i, "templates") for i in (
            # user dir
            os.path.join(os.path.expanduser('~'), '.py2pack'),
            platformdirs.user_data_dir(appname="py2pack"),
            platformdirs.user_config_dir(appname="py2pack"),
            # usually inside the site-packages dir
            os.path.dirname(__file__),
            # system wide dir
            *platformdirs.site_data_dir(appname="py2pack", multipath=True).split(":"),
        )
    ])


def list_packages(args=None):
    """query the "Simple API" of PYPI for all packages and print them."""
    print('listing all PyPI packages...')
    with requests.get('https://pypi.org/simple/') as r:
        html = r.text
    simplere = re.compile(r'<a href="/simple/.+">(.*)</a>')
    for package in simplere.findall(html):
        print(package)


def search(args):
    print('searching for package {0}...'.format(args.name))
    for hit in pypi_search.search.find_packages(args.name):
        print('found {0}-{1}'.format(hit['name'], hit['version']))


def show(args):
    fetch_data(args)
    print('showing package {0}...'.format(args.fetched_data['info']['name']))
    pprint.pprint(args.fetched_data)


def fetch(args):
    fetch_data(args)
    url = newest_download_url(args)
    if not url:
        print("unable to find a source release for {0}!".format(args.name))
        sys.exit(1)
    print('downloading package {0}-{1}...'.format(args.name, args.version))
    print('from {0}'.format(url['url']))

    with requests.get(url['url']) as r:
        with open(url['filename'], 'wb') as f:
            f.write(r.content)


def _canonicalize_setup_data(data):

    if data.get('build-system', None):
        # PEP 518: 'requires' field is mandatory
        data['build_requires'] = py2pack.requires._requirements_sanitize(
            data['build-system']['requires'])
    elif data.get('setup_requires', None):
        # Setuptools, deprecated.
        setup_requires = data.pop('setup_requires')
        # setup_requires may be a string, convert to list of strings:
        if isinstance(setup_requires, str):
            setup_requires = setup_requires.splitlines()
        # canonicalize to build_requires
        data["build_requires"] = ['setuptools', 'wheel'] + \
            py2pack.requires._requirements_sanitize(setup_requires)
    else:
        # no build_requires means most probably legacy setuptools
        data["build_requires"] = ['setuptools']
    if 'setuptools' in data['build_requires'] and 'wheel' not in data['build_requires']:
        data['build_requires'] += ['wheel']

    install_requires = (
        get_pyproject_table(data, "project.dependencies") or
        get_pyproject_table(data, "tool.flit.metadata.requires") or
        data.get("install_requires", None))
    if install_requires:
        # Setuptools or PEP 621
        # Setuptools: install_requires may be a string, convert to list of strings:
        if isinstance(install_requires, str):
            install_requires = install_requires.splitlines()
        data["install_requires"] = \
            py2pack.requires._requirements_sanitize(install_requires)
    else:
        # Poetry
        try:
            if 'dependencies' in data['tool']['poetry']:
                warnings.warn("The package defines its dependencies in the "
                              "[tool.poetry.dependencies] table of pyproject.toml. "
                              "Automatic parsing of the poetry format is not "
                              "implemented yet. You must add the requirements "
                              "manually.")
        except KeyError:
            pass

    tests_require = (
        get_pyproject_table(data, "project.optional-dependencies.test") or
        get_pyproject_table(data, "tool.flit.metadata.requires-extra.test") or
        get_pyproject_table(data, "tool.poetry.group.test.dependencies") or
        data.get("tests_require", None))
    if tests_require:
        # Setuptools: tests_require may be a string, convert to list of strings:
        if isinstance(tests_require, str):
            tests_require = tests_require.splitlines()
        data["tests_require"] = \
            py2pack.requires._requirements_sanitize(tests_require)

    extras_require = (
        get_pyproject_table(data, "project.optional-dependencies") or
        get_pyproject_table(data, "tool.flit.metadata.requires-extra") or
        data.get("extras_require", None))
    if extras_require:
        data["extras_require"] = dict()
        for (key, value) in extras_require.items():
            # do not add the test requirements to the regular suggestions
            if key == "test":
                continue
            # Setuptools: extras_require value may be a string, convert to list of strings:
            if isinstance(value, str):
                extras_require[key] = value.splitlines()
            data["extras_require"][key] = \
                py2pack.requires._requirements_sanitize(extras_require[key])

    if data.get('data_files', None):
        # data_files may be a sequence of files without a target directory:
        if len(data["data_files"]) and isinstance(data["data_files"][0], str):
            data["data_files"] = [("", data["data_files"])]
        # directory paths may be relative to the installation prefix:
        prefix = sys.exec_prefix if "is_extension" in data else sys.prefix
        data["data_files"] = [
            (dir if (len(dir) and dir[0] == '/') else os.path.join(prefix, dir), files)
            for (dir, files) in data["data_files"]]

    console_scripts = get_setuptools_scripts(data)
    console_scripts += list(get_pyproject_table(data, "project.scripts", notfound={}).keys())
    console_scripts += list(get_pyproject_table(data, "project.gui-scripts", notfound={}).keys())
    console_scripts += list(get_pyproject_table(data, "tool.flit.scripts", notfound={}).keys())
    console_scripts += list(get_pyproject_table(data, "tool.poetry.scripts", notfound={}).keys())
    if console_scripts:
        # remove duplicates, preserver order
        data["console_scripts"] = list(dict.fromkeys(console_scripts))

    # Standards says, that keys must be lowercase but not even PyPA adheres to it
    homepage = (get_pyproject_table(data, 'project.urls.homepage') or
                get_pyproject_table(data, 'project.urls.Homepage') or
                get_pyproject_table(data, 'project.urls.Source') or
                get_pyproject_table(data, 'project.urls.GitHub') or
                get_pyproject_table(data, 'project.urls.Repository') or
                data.get('home_page', None))
    if homepage:
        data['home_page'] = homepage

    # remove doc_files: None
    if data.get('doc_files', []) is None:
        data.pop('doc_files')

    # remove license_files: None
    if data.get('license_files', []) is None:
        data.pop('license_files')


def _quote_shell_metacharacters(string):
    shell_metachars_re = re.compile(r"[|&;()<>\s]")
    if re.search(shell_metachars_re, string):
        return "'" + string + "'"
    return string


def _augment_data_from_tarball(args, filename, data):
    docs_re = re.compile(r"{0}-{1}\/((?:AUTHOR|ChangeLog|CHANGES|NEWS|README).*)".format(args.name, args.version), re.IGNORECASE)
    license_re = re.compile(r"{0}-{1}\/((?:COPYING|LICENSE).*)".format(args.name, args.version), re.IGNORECASE)

    data_pyproject = parse_pyproject(filename)
    if data_pyproject is not None and "license" in data and data["license"] in SPDX_LICENSES:
        # Trust the PyPI Metadata and don't try to update with a possible non SPDX identifier
        data_pyproject.pop("license", None)
    data.update(data_pyproject)

    try:
        buildrequires = data['build-system']['requires']
    except KeyError:
        # No build system specified in pyproject.toml: legacy setuptools
        buildrequires = ['setuptools']

    if any(['setuptools' in br for br in buildrequires]):
        try:
            data_archive = meta_utils.from_archive(filename)
            data.update(data_archive['data'])
        except Exception as exc:
            warnings.warn("Could not get setuptools information from tarball {}: {}. "
                          "Valuable information for the generation might be missing."
                          .format(filename, exc))
    else:
        try:
            mdata = get_metadata(filename)
            data.update(mdata)
        except Exception as exc:
            warnings.warn("Could not get metadata information from tarball {}: {}. "
                          "Valuable information for the generation might be missing."
                          .format(filename, exc))

    names = _get_archive_filelist(filename)
    _canonicalize_setup_data(data)

    for name in names:
        match_docs = re.match(docs_re, name)
        match_license = re.match(license_re, name)
        if match_docs:
            data.setdefault('doc_files', []).append(
                _quote_shell_metacharacters(match_docs.group(1)))
        if match_license:
            data.setdefault('license_files', []).append(
                _quote_shell_metacharacters(match_license.group(1))
            )
        # Very broad check for testsuites
        if "test" in name.lower():
            data["testsuite"] = True


def _license_from_classifiers(data):
    """try to get a license from the classifiers"""
    classifiers = data.get('classifiers', [])
    found_license = None
    for c in classifiers:
        if c.startswith("License :: OSI Approved :: "):
            found_license = c.replace("License :: OSI Approved :: ", "")
    return found_license


def _normalize_license(data):
    """try to get SPDX license"""
    license = data.get('license', None)
    if not license:
        # try to get license from classifiers
        license = _license_from_classifiers(data)
    if license:
        if license in SPDX_LICENSES.keys():
            data['license'] = SPDX_LICENSES[license]
        else:
            data['license'] = "%s (FIXME:No SPDX)" % (license)
    else:
        data['license'] = "FIXME-UNKNOWN"


def _prepare_template_env(template_dir):
    # setup jinja2 environment with custom filters
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    env.filters['parenthesize_version'] = \
        lambda s: re.sub('([=<>]+)(.+)', r' (\1 \2)', s)
    env.filters['basename'] = \
        lambda s: s[s.rfind('/') + 1:]
    return env


def _get_source_url(pypi_name, filename):
    """get the source url"""
    # example: https://files.pythonhosted.org/packages/source/u/ujson/ujson-1.2.3.tar.gz
    return 'https://files.pythonhosted.org/packages/source/{}/{}/{}'.format(
        pypi_name[0], pypi_name, filename)


def generate(args):
    # TODO (toabctl): remove this is a later release
    if args.run:
        warnings.warn("the '--run' switch is deprecated and a noop",
                      DeprecationWarning)

    fetch_local_data(args)
    if not args.template:
        args.template = file_template_list()[0]
    if not args.filename:
        args.filename = "python-" + args.name + '.' + args.template.rsplit('.', 1)[1]   # take template file ending
    print('generating spec file for {0}...'.format(args.name))
    data = args.fetched_data['info']
    durl = newest_download_url(args)
    source_url = data['source_url'] = (args.source_url or (durl and durl['url']))
    data['year'] = datetime.datetime.now().year                             # set current year
    data['user_name'] = pwd.getpwuid(os.getuid())[4]                        # set system user (packager)
    data['summary_no_ending_dot'] = re.sub(r'(.*)\.', r'\g<1>', data.get('summary')) if data.get('summary') else ""

    # If package name supplied on command line differs in case from PyPI's one
    # then package archive will be fetched but the name will be the one from PyPI.
    # Eg. send2trash vs Send2Trash. Check that.
    tr = str.maketrans('-.', '__')
    version = args.version
    name = args.name
    default_source = '%{name}-%{version}.*'
    source_glob = args.source_glob or default_source
    data_name = data['name'] or name

    tarball_file = []
    for __name in (name, name.translate(tr), data_name, data_name.translate(tr)):
        tarball_file.extend(glob.glob(replace_string(source_glob, {'name': __name, 'version': version})))
        if tarball_file:
            break

    if tarball_file:                                                        # get some more info from that
        tarball_file = tarball_file[0]
        _augment_data_from_tarball(args, tarball_file, data)

    else:
        warnings.warn("No tarball for {} in version {} found. Valuable "
                      "information for the generation might be missing."
                      "".format(args.name, args.version))
        tarball_file = args.name + '-' + args.version + '.zip'

    if not source_url:
        data['source_url'] = os.path.basename(tarball_file)

    _normalize_license(data)

    env = _prepare_template_env(_get_template_dirs())
    template = env.get_template(args.template)
    result = template.render(data).encode('utf-8')                          # render template and encode properly
    outfile = open(args.filename, 'wb')                                     # write result to spec file
    try:
        outfile.write(result)
    finally:
        outfile.close()


def fix_data(data):
    extra_from_req = re.compile(r'''\bextra\s+==\s+["']([^"']+)["']''')
    extras = []
    data_info = data["info"]
    requires_dist = data_info["requires_dist"] or []
    provides_extra = data_info["provides_extra"] or []
    if requires_dist is not None:
        for required_dist in requires_dist:
            req = Requirement(required_dist)
            if found := re.search(extra_from_req, str(req.marker)):
                extras.add(found.group(1))
    provides_extra = list(sorted(set([*extras, *provides_extra])))
    data_info["requires_dist"] = requires_dist
    data_info["provides_extra"] = provides_extra
    data_info["classifiers"] = (data_info["classifiers"] or [])


def fetch_local_data(args):
    localfile = args.localfile
    local = args.local

    if not localfile and local:
        localfile = os.path.join(f'{args.name}.egg-info', 'PKG-INFO')
    if os.path.isfile(localfile):
        try:
            data = pypi_json_file(localfile)
        except json.decoder.JSONDecodeError:
            data = pypi_archive_file(localfile)
            if data is None:
                data = pypi_text_file(localfile)
        args.fetched_data = data
        args.version = args.fetched_data['info']['version']
        fix_data(data)
    else:
        fetch_data(args)


def fetch_data(args):
    data = args.fetched_data = pypi_json(args.name, args.version)
    urls = data.get('urls', [])
    if len(urls) == 0:
        print(f"unable to find a suitable release for {args.name}!")
        sys.exit(1)
    else:
        args.version = data['info']['version']                 # return current release number
    fix_data(data)


def newest_download_url(args):
    """check but do not use the url delivered by pypi. that url contains a hash and
    needs to be adjusted with every package update. Instead use
    the pypi.io url
    """
    if not hasattr(args, "fetched_data"):
        return {}
    for release in args.fetched_data['urls']:     # Check download URLs in releases
        if release['packagetype'] == 'sdist':                      # Found the source URL we care for
            release['url'] = _get_source_url(args.name, release['filename'])
            return release
    # No PyPI tarball release, let's see if an upstream download URL is provided:
    data = args.fetched_data['info']
    if 'download_url' in data and data['download_url']:
        url = data['download_url']
        return {'url': url,
                'filename': os.path.basename(url)}
    return {}                                                               # We're all out of bubblegum


def file_template_list():
    template_files = []
    for d in _get_template_dirs():
        template_files += [f for f in os.listdir(d) if not f.startswith('.')]
    return template_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(py2pack_version.version))
    parser.add_argument('--proxy', help='HTTP proxy to use')
    subparsers = parser.add_subparsers(title='commands')

    parser_list = subparsers.add_parser('list', help='list all packages on PyPI')
    parser_list.set_defaults(func=list_packages)

    parser_search = subparsers.add_parser('search', help='search for packages on PyPI')
    parser_search.add_argument('name', help='package name (with optional version)')
    parser_search.set_defaults(func=search)

    parser_show = subparsers.add_parser('show', help='show metadata for package')
    parser_show.add_argument('name', help='package name')
    parser_show.add_argument('version', nargs='?', help='package version (optional)')
    parser_show.set_defaults(func=show)

    parser_fetch = subparsers.add_parser('fetch', help='download package source tarball from PyPI')
    parser_fetch.add_argument('name', help='package name')
    parser_fetch.add_argument('version', nargs='?', help='package version (optional)')
    parser_fetch.add_argument('--source-url', default=None, help='source url')
    parser_fetch.set_defaults(func=fetch)

    parser_generate = subparsers.add_parser('generate', help='generate RPM spec or DEB dsc file for a package')
    parser_generate.add_argument('name', help='package name')
    parser_generate.add_argument('version', nargs='?', help='package version (optional)')
    parser_generate.add_argument('--source-url', default=None, help='source url')
    parser_generate.add_argument('--source-glob', help='source glob template')
    parser_generate.add_argument('--local', action='store_true', help='build from local package')
    parser_generate.add_argument('--localfile', default='', help='path to the local PKG-INFO or json metadata')
    parser_generate.add_argument('-t', '--template', choices=file_template_list(), default=DEFAULT_TEMPLATE, help='file template')
    parser_generate.add_argument('-f', '--filename', help='spec filename (optional)')
    # TODO (toabctl): remove this is a later release
    parser_generate.add_argument(
        '-r', '--run', action='store_true',
        help='DEPRECATED and noop. will be removed in future releases!')
    parser_generate.set_defaults(func=generate)

    parser_help = subparsers.add_parser('help', help='show this help')
    parser_help.set_defaults(func=lambda args: parser.print_help())

    args = parser.parse_args()

    # set HTTP proxy if one is provided
    if args.proxy:
        with requests.get(args.proxy) as r:
            if not r.ok:
                print('the proxy \'{0}\' is not responding'.format(args.proxy))
                sys.exit(1)
        os.environ["HTTP_PROXY"] = args.proxy
        os.environ["HTTPS_PROXY"] = args.proxy

    if 'func' not in args:
        sys.exit(parser.print_help())
    args.func(args)


# fallback if run directly
if __name__ == '__main__':
    main()
