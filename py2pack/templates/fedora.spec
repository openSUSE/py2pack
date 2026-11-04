%global pypi_name {{ name }}
%global python_name python3-%{pypi_name}
{%- set build_reqs = build_requires or [] %}
{%- set runtime_reqs = (requires or []) + (install_requires or []) %}
{%- set has_tests = testsuite or test_suite or tests_require %}
{%- set scripts_or_console_scripts = (
            (scripts|map('basename')|list if scripts else []) +
            (console_scripts if console_scripts else []))|unique|list %}
{%- if has_tests %}

%bcond_without test
{%- endif %}

Name:           python-%{pypi_name}
Version:        {{ version }}
Release:        %autorelease
Summary:        {{ summary }}

# Check the generated license identifier against Fedora's licensing guidelines.
License:        {{ license }}
URL:            {{ home_page }}
Source:         {{ source_url|replace(version, '%{version}') }}
{%- if not has_ext_modules %}
BuildArch:      noarch
{%- endif %}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
{%- if has_ext_modules %}
BuildRequires:  gcc
{%- endif %}
{%- for req in build_reqs|unique|sort %}
BuildRequires:  {{ req|fedora_requirement }}
{%- endfor %}
{%- if source_url.endswith('.zip') %}
BuildRequires:  unzip
{%- endif %}
{%- if has_tests %}

%if %{with test}
{%- for req in (runtime_reqs + (tests_require or []) + ['pytest'])|unique|sort %}
{%- if req not in build_reqs %}
BuildRequires:  {{ req|fedora_requirement }}
{%- endif %}
{%- endfor %}
%endif
{%- endif %}

%global _description %{expand:
{{ description }}}

%description %_description

%package -n %{python_name}
Summary:        %{summary}
{%- for req in runtime_reqs|unique|sort %}
Requires:       {{ req|fedora_requirement }}
{%- endfor %}
{%- if extras_require %}
{%- for req in extras_require.values()|sum(start=[])|unique|sort %}
Suggests:       {{ req|fedora_requirement }}
{%- endfor %}
{%- endif %}

%description -n %{python_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
# Replace '*' with the actual importable module names before submission.
%pyproject_save_files '*'
{%- if has_tests %}

%check
%if %{with test}
# Adjust the test runner and arguments to match the upstream test suite.
%pytest
%endif
{%- endif %}

%files -n %{python_name} -f %{pyproject_files}
{%- for script in scripts_or_console_scripts|sort %}
%{_bindir}/{{ script }}
{%- endfor %}

%changelog
%autochangelog
