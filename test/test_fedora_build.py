# Licensed under the Apache License, Version 2.0. See LICENSE for details.
"""Opt-in RPM build tests. Run in Fedora with PY2PACK_TEST_FEDORA_BUILDS=1."""

import os
from pathlib import Path
import shutil
import subprocess
import tarfile

import pytest

import py2pack


pytestmark = pytest.mark.skipif(
    os.environ.get('PY2PACK_TEST_FEDORA_BUILDS') != '1' or shutil.which('rpmbuild') is None,
    reason='Fedora RPM builds are opt-in and require rpmbuild')


@pytest.mark.parametrize('kind, with_tests', [
    ('legacy', True), ('pep517', True), ('native', True), ('console', True), ('pep517', False),
])
def test_fedora_rpm_build(tmp_path, kind, with_tests):
    fedora = subprocess.check_output(['rpm', '--eval', '%{?fedora}'], text=True).strip()
    if not fedora:
        pytest.skip('Fedora RPM macros are required')

    source = tmp_path / 'demo-1.0'
    (source / 'demo').mkdir(parents=True)
    (source / 'demo' / '__init__.py').write_text('VALUE = 42\n\ndef main():\n    print(VALUE)\n')
    (source / 'LICENSE').write_text('SPDX-License-Identifier: MIT\n')
    (source / 'README.md').write_text('A package for testing Fedora RPM generation.\n')
    (source / 'example.txt').write_text('Example installed data.\n')
    (source / 'tests').mkdir()
    test = 'from demo import VALUE\n\ndef test_value():\n    assert VALUE == 42\n'
    if kind == 'native':
        test += '\ndef test_native():\n    import demo.native\n'
    (source / 'tests' / 'test_demo.py').write_text(test)

    build_system = ('[build-system]\nrequires = ["setuptools", "wheel"]\n'
                    'build-backend = "setuptools.build_meta"\n')
    if kind in ['legacy', 'native']:
        extension = ''
        if kind == 'native':
            (source / 'native.c').write_text(
                '#include <Python.h>\n'
                'static struct PyModuleDef module = {\n'
                '    PyModuleDef_HEAD_INIT, "native", NULL, -1, NULL\n'
                '};\n'
                'PyMODINIT_FUNC PyInit_native(void) { return PyModule_Create(&module); }\n')
            extension = ', ext_modules=[Extension("demo.native", ["native.c"])]'
            (source / 'pyproject.toml').write_text(build_system)
        (source / 'setup.py').write_text(
            'from setuptools import setup, Extension\n'
            'setup(name="demo", version="1.0", packages=["demo"], license="MIT",\n'
            '      data_files=[("share/demo", ["example.txt"])]' + extension + ')\n')
    else:
        project = ('\n[project]\nname = "demo"\nversion = "1.0"\nlicense = "MIT"\n')
        scripts = ''
        if kind == 'console':
            project += '\n[project.scripts]\ndemo-cli = "demo:main"\n'
            scripts = 'script-files = ["bin/demo-legacy"]\n'
            (source / 'bin').mkdir()
            (source / 'bin' / 'demo-legacy').write_text('#!/usr/bin/python3\nprint(42)\n')
            (source / 'bin' / 'demo-legacy').chmod(0o755)
        (source / 'pyproject.toml').write_text(
            build_system + project + '\n[tool.setuptools]\npackages = ["demo"]\n' + scripts +
            '\n[tool.setuptools.data-files]\n"share/demo" = ["example.txt"]\n')
        assert not (source / 'setup.py').exists()

    topdir = tmp_path / 'rpmbuild'
    (topdir / 'SOURCES').mkdir(parents=True)
    with tarfile.open(topdir / 'SOURCES' / 'demo-1.0.tar.gz', 'w:gz') as archive:
        archive.add(source, arcname=source.name)

    template_dir = Path(py2pack.__file__).parent / 'templates'
    template = py2pack._prepare_template_env(str(template_dir)).get_template('fedora.spec')
    spec = tmp_path / 'demo.spec'
    spec.write_text(template.render(
        name='demo', version='1.0', summary='Demo package', license='MIT',
        home_page='https://example.org/demo', source_url='https://example.org/demo-1.0.tar.gz',
        description='A demonstration package.', build_requires=['setuptools', 'wheel'],
        python_modules=['demo'], has_ext_modules=(kind == 'native'),
        scripts=['bin/demo-legacy'] if kind == 'console' else None,
        console_scripts=['demo-cli'] if kind == 'console' else None,
        testsuite=True, tests_require=['pytest'], doc_files=['README.md'], license_files=['LICENSE'],
        data_files=[('/usr/share/demo', ['example.txt'])]))
    command = ['rpmbuild', '-ba', '--define', '_topdir ' + str(topdir), str(spec)]
    if not with_tests:
        command.extend(['--without', 'test'])
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, timeout=180)
    (tmp_path / 'build.log').write_text(result.stdout)
    assert result.returncode == 0, result.stdout
    assert (' passed' in result.stdout) == with_tests

    rpm = next((topdir / 'RPMS').rglob('python3-demo-1.0-*.rpm'))
    files = subprocess.check_output(['rpm', '-qlp', str(rpm)], text=True).splitlines()
    assert any(path.endswith('/demo/__init__.py') for path in files)
    assert any(path.endswith('/README.md') for path in files)
    assert any(path.endswith('/LICENSE') for path in files)
    assert '/usr/share/demo/example.txt' in files
    if kind == 'console':
        assert '/usr/bin/demo-cli' in files
        assert '/usr/bin/demo-legacy' in files
        assert not any(path.startswith('/usr/bin/bin/') for path in files)
    if kind == 'native':
        assert any('/demo/native.' in path and path.endswith('.so') for path in files)
    architecture = subprocess.check_output(['rpm', '-qp', '--qf', '%{ARCH}', str(rpm)], text=True)
    assert (architecture == 'noarch') == (kind != 'native')
