%define pypi_name {{ name }}
%define python_name python3-%{pypi_name}
Name:           python-%{pypi_name}
Version:        {{ version }}
Release:        %autorelease
Summary:        {{ summary }}

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        {{ license }}
URL:            {{ home_page }}
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel {%- if requires_python %} {{ requires_python }} {% endif %}
{%- for req in requires %}
BuildRequires:  {{ req|rpm_format_requires("python-") }}
Requires:       {{ req|rpm_format_requires }}
{%- endfor %}
{%- for req in install_requires %}
BuildRequires:  {{ req|rpm_format_requires("python-") }}
Requires:       {{ req|rpm_format_requires("python-") }}
{%- endfor %}
{%- endif %}
{%- if tests_require and tests_require is not none %}
{%- for req in tests_require|sort|reject("in",build_requires|sort) %}
BuildRequires:  %{python_module {{ req }}}
{%- endfor %}
{%- endif %}
%endif
# /SECTION
{%- endif %}
{%- if source_url.endswith('.zip') %}
BuildRequires:  unzip
{%- endif %}
BuildRequires:  fdupes
{%- if install_requires and install_requires is not none %}
{%- for req in install_requires|sort %}
Requires:       %{python_module {{ req }}}
{%- endfor %}
{%- endif %}
{%- if extras_require and extras_require is not none %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       {{ req|rpm_format_requires("python-") }}
{%- endfor %}
{%- endfor %}
{%- endif %}
{%- if not has_ext_modules %}
BuildArch:      noarch
{%- endif %}

# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
{{ description }}}

%description %_description

%package -n %{python_name}
Summary:        %{summary}

%description -n %{python_name} %_description


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%pyproject_wheel


%install
%pyproject_install
{%- set scripts_or_console_scripts = (
            (scripts|map('basename')|list if scripts and scripts is not none else []) +
            (console_scripts if console_scripts and console_scripts is not none else [])) %}
#{%- for script in scripts_or_console_scripts %}
#%python_clone -a %{buildroot}%{_bindir}/{{ script }}
#{%- endfor %}
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto


{%- if testsuite or test_suite %}
%if %{with test}
%check
{%- if has_ext_modules %}
%pytest_arch
{%- else %}
%pytest
{%- endif %}
%endif
{%- endif %}

%files -n %{python_name} -f %{pyproject_files}

%changelog
%autochangelog


