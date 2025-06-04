from email import parser
from importlib import metadata
import json
from io import TextIOWrapper
import tarfile
import os
import pwd
import zipfile
from os.path import join, basename, isfile
import re
from packaging.requirements import Requirement


def lowercase_dict(d):
    ret = {}
    for key, value in d.items():
        ret[str(key).lower()] = value
    return ret


def get_homepage(urls):
    try:
        urls = lowercase_dict(urls)
        for page in ('homepage', 'source', 'github', 'repository', 'gitlab'):
            if page in urls:
                return urls[page]
    except Exception:
        return None


def pypi_text_file(pkg_info_path):
    # open PKG-INFO file and parse
    pkg_info_file = open(pkg_info_path, 'r')
    text = pypi_text_stream(pkg_info_file)
    pkg_info_file.close()
    return text


def pypi_text_stream(pkg_info_stream):
    # parse PKG-INFO stream
    pkg_info_lines = parser.Parser().parse(pkg_info_stream)
    return pypi_text_items(pkg_info_lines.items())


def pypi_text_metaextract(library):
    # parse metadata from python module which already exists
    pkg_info_lines = metadata.metadata(library)
    return pypi_text_items(pkg_info_lines.items())


def pypi_text_items(pkg_info_items):
    # parse PKG-INFO lines
    pkg_info_dict = {}
    for key, value in pkg_info_items:
        key = key.lower().replace('-', '_')
        if key in {'requires_dist', 'provides_extra'}:
            val = dict.setdefault(pkg_info_dict, key, [])
            val.append(value)
        elif key in {'classifier'}:
            val = dict.setdefault(pkg_info_dict, key + 's', [])
            val.append(value)
        elif key in {'project_url'}:
            key1, val = value.split(',', 1)
            pkg_info_dict.setdefault(key + 's', {})[key1.strip()] = val.strip()
        else:
            pkg_info_dict[key] = value
    return {'info': pkg_info_dict, 'urls': []}


def pypi_json_file(file_path):
    # parse pypi json file
    json_file = open(file_path, 'r')
    js = pypi_json_stream(json_file)
    json_file.close()
    return js


def pypi_json_stream(json_stream):
    # parse pypi json stream
    js = json.load(json_stream)
    if 'info' not in js:
        js = {'info': js}
    if 'urls' not in js:
        js['urls'] = []
    return js


def _check_if_pypi_archive_file(path):
    # check if archive is python source
    return path.count('/') == 1 and basename(path) == 'PKG-INFO'


def pypi_archive_file(file_path):
    # try to extract metadata from tar archive
    if tarfile.is_tarfile(file_path):
        with tarfile.open(file_path, 'r') as archive:
            for member in archive.getmembers():
                if _check_if_pypi_archive_file(member.name):
                    return pypi_text_stream(TextIOWrapper(archive.extractfile(member), encoding='utf-8'))
    # try to extract metadata from zip archive
    elif zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as archive:
            for member in archive.namelist():
                if _check_if_pypi_archive_file(member):
                    return pypi_text_stream(TextIOWrapper(archive.open(member), encoding='utf-8'))
    else:
        raise TypeError("Can not extract '%s'. Not a tar or zip file" % file_path)
    raise KeyError('PKG-INFO not found on archive ' + file_path)


def fetch_local_data(args):
    # autodetect localfile name and type and parse
    localfile = args.localfile
    local = args.local
    # set localarchive argument
    args.localarchive = None
    if not localfile and local:
        try:
            args.fetched_data = pypi_text_metaextract(args.name)
            return True
        except metadata.PackageNotFoundError:
            localfile = join(f'{args.name}.egg-info', 'PKG-INFO')
    if isfile(localfile):
        try:
            data = pypi_archive_file(localfile)
            args.localarchive = localfile
        except TypeError:
            try:
                data = pypi_json_file(localfile)
            except json.decoder.JSONDecodeError:
                data = pypi_text_file(localfile)
        args.fetched_data = data
        return True
    return False


def fix_info(data_info):
    # fix requires_dist
    requires_dist = data_info.get("requires_dist", None) or []
    # fix provides_extra
    provides_extra = data_info.get("provides_extra", None) or []
    extra_from_req = re.compile(r'''\bextra\s+==\s+["']([^"']+)["']''')
    # add additional provides_extra from requires_dist
    for required_dist in requires_dist:
        req = Requirement(required_dist)
        if found := extra_from_req.search(str(req.marker)):
            provides_extra.append(found.group(1))
    # provides_extra must be unique list
    provides_extra = list(sorted(set(provides_extra)))
    # fix classifiers
    classifiers = data_info.get("classifiers", None) or []
    # get project_urls dictionary
    try:
        urls = dict(data_info.get('project_urls', None))
    except TypeError:
        urls = {}
    # fix homepage
    if 'home_page' not in data_info:
        home_page = get_homepage(urls) or data_info.get('project_url', None)
        if home_page:
            data_info['home_page'] = home_page
    # set fixed requires_dist
    data_info["requires_dist"] = requires_dist
    # set fixed provides_extra
    data_info["provides_extra"] = provides_extra
    # set fixed classifiers
    data_info["classifiers"] = classifiers
    # set fixed project_urls
    data_info['project_urls'] = urls


# get username
def get_user_name():
    pwuid = pwd.getpwuid(os.getuid())
    gecos = pwuid.pw_gecos  # or pwd.getpwuid(os.getuid())[4]
    name = pwuid.pw_name  # or pwd.getpwuid(os.getuid())[0]
    return gecos or name
