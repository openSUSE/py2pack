# Licensed under the Apache License, Version 2.0. See LICENSE for details.
"""Offline regression tests for generated Fedora specs."""

import os

import pytest

import py2pack


@pytest.fixture
def render_fedora():
    template_dir = os.path.join(os.path.dirname(py2pack.__file__), 'templates')
    template = py2pack._prepare_template_env(template_dir).get_template('fedora.spec')

    def render(**overrides):
        data = dict(name='demo', version='1.0', summary='Demo package',
                    license='MIT', home_page='https://example.org/demo',
                    source_url='https://example.org/demo-1.0.tar.gz',
                    description='A demonstration package.')
        data.update(overrides)
        return template.render(data)

    return render


@pytest.mark.parametrize('scripts', [
    {}, {'scripts': None}, {'scripts': []}, {'console_scripts': None},
])
def test_fedora_missing_scripts(render_fedora, scripts):
    spec = render_fedora(**scripts)
    assert '%pyproject_install' in spec
    assert '%{_bindir}/' not in spec


@pytest.mark.parametrize('extension', ['tar.gz', 'tar.xz', 'zip'])
def test_fedora_source_url(render_fedora, extension):
    url = 'https://example.org/custom/demo-1.0.' + extension
    spec = render_fedora(source_url=url)
    assert 'Source:         https://example.org/custom/demo-%{version}.' + extension in spec
    assert ('BuildRequires:  unzip' in spec) == (extension == 'zip')


@pytest.mark.parametrize('requirement, expected', [
    ('hatchling >= 1.0', 'python3dist(hatchling) >= 1.0'),
    ('Jinja2', 'python3dist(jinja2)'),
    ('flit_core >= 3', 'python3dist(flit-core) >= 3'),
    ('zope.interface == 7.0', 'python3dist(zope-interface) = 7.0'),
    ('foo > 1', 'python3dist(foo) > 1'),
    ('foo < 2', 'python3dist(foo) < 2'),
    ('foo <= 2', 'python3dist(foo) <= 2'),
])
def test_fedora_build_dependencies(render_fedora, requirement, expected):
    spec = render_fedora(build_requires=[requirement])
    assert 'BuildRequires:  ' + expected in spec
    assert 'BuildRequires:  python3-devel' in spec
    assert 'BuildRequires:  pyproject-rpm-macros' in spec
    assert '%generate_buildrequires\n%pyproject_buildrequires' in spec
    assert '%pyproject_wheel' in spec
    assert '%pyproject_install' in spec


def test_fedora_runtime_dependencies_belong_to_subpackage(render_fedora):
    spec = render_fedora(requires=['legacy >= 1'], install_requires=['requests >= 2'],
                         extras_require={'extra': ['colorama']})
    source, binary = spec.split('%package -n %{python_name}', 1)
    assert not any(line.startswith(('Requires:', 'Suggests:')) for line in source.splitlines())
    assert 'Requires:       python3dist(legacy) >= 1' in binary
    assert 'Requires:       python3dist(requests) >= 2' in binary
    assert 'Suggests:       python3dist(colorama)' in binary


@pytest.mark.parametrize('metadata', [
    {'testsuite': True}, {'test_suite': 'tests'}, {'tests_require': ['coverage']},
])
def test_fedora_conditional_tests(render_fedora, metadata):
    spec = render_fedora(install_requires=['requests'], **metadata)
    assert '%bcond_without test' in spec
    test_dependencies = spec.split('%if %{with test}', 1)[1].split('%endif', 1)[0]
    assert 'BuildRequires:  python3dist(requests)' in test_dependencies
    assert 'BuildRequires:  python3dist(pytest)' in test_dependencies
    if metadata.get('tests_require'):
        assert 'BuildRequires:  python3dist(coverage)' in test_dependencies
    assert '%check\n%if %{with test}' in spec
    assert '\n%pytest\n%endif' in spec
    assert '%pytest_arch' not in spec  # This is an openSUSE macro, not a Fedora one.


def test_fedora_distinct_build_and_test_constraints(render_fedora):
    spec = render_fedora(build_requires=['poetry-core >= 1.5.0'],
                         tests_require=['poetry-core == 1.6.1'])
    assert 'BuildRequires:  python3dist(poetry-core) >= 1.5.0' in spec
    assert 'BuildRequires:  python3dist(poetry-core) = 1.6.1' in spec


def test_fedora_no_test_suite(render_fedora):
    spec = render_fedora(tests_require=None)
    assert '%{with test}' not in spec
    assert '%check' not in spec
    assert 'python3dist(pytest)' not in spec


@pytest.mark.parametrize('native', [False, True])
def test_fedora_native_extensions(render_fedora, native):
    spec = render_fedora(has_ext_modules=native, is_extension=not native, testsuite=True)
    assert ('BuildArch:      noarch' in spec) == (not native)
    assert ('BuildRequires:  gcc' in spec) == native
    assert '%pyproject_save_files' in spec
    assert '%files -n %{python_name} -f %{pyproject_files}' in spec
    assert 'sitearch}/*' not in spec
    assert 'sitelib}/*' not in spec
    assert 'archlib' not in spec


def test_fedora_script_names_and_duplicates(render_fedora):
    spec = render_fedora(scripts=['bin/legacy-cli', 'scripts/shared-cli'],
                         console_scripts=['demo-cli', 'shared-cli'])
    for name in ['legacy-cli', 'demo-cli', 'shared-cli']:
        assert spec.count('%{_bindir}/' + name) == 1
    assert '%{_bindir}/bin/' not in spec
    assert '%{_bindir}/scripts/' not in spec
    assert '%{__mv}' not in spec
    assert '%{__ln_s}' not in spec
    assert '+auto' not in spec


@pytest.mark.parametrize('licenses, flag', [(['LICENSE'], '-L'), (None, '-l')])
def test_fedora_explicit_module_manifest(render_fedora, licenses, flag):
    spec = render_fedora(python_modules=['second', 'first'], license_files=licenses)
    assert '%pyproject_save_files ' + flag + ' first second' in spec
    assert "save_files '*'" not in spec
    assert 'guessed' not in spec


def test_fedora_guessed_module_name_is_flagged(render_fedora):
    spec = render_fedora(name='Demo.Project-name')
    assert '# Verify this import name, guessed from the distribution name.' in spec
    assert '%pyproject_save_files -l demo_project_name' in spec


def test_fedora_docs_licenses_and_data(render_fedora):
    spec = render_fedora(doc_files=['README.md', 'AUTHORS'], license_files=['LICENSE'],
                         data_files=[('/usr/share/demo', ['data/example.txt']),
                                     ('/etc/demo/', ['config/demo.conf'])])
    files = spec.split('%files -n %{python_name} -f %{pyproject_files}', 1)[1]
    assert '%doc README.md AUTHORS' in files
    assert '%license LICENSE' in files
    assert '%{_datadir}/demo/example.txt' in files
    assert '%{_sysconfdir}/demo/demo.conf' in files
    assert '%dir %{_datadir}' not in files


def test_fedora_no_legacy_boilerplate(render_fedora):
    spec = render_fedora()
    for text in ['python2', '%py3_build', '%py3_install', 'with_dnf',
                 'common_description', 'Group:', 'BuildRoot:', '%clean', '%defattr', 'fdupes']:
        assert text not in spec
