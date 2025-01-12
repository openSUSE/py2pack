%define pypi_name {{ name }}
%define python_name python3-%{pypi_name}
Name:           python-%{pypi_name}
Version:        {{ version }}
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        {{ summary_singleline }}

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        {{ license_singleline }}
URL:            {{ home_page_singleline }}
Source:         {{ source_url_singleline|replace(version, '%{version}') }}

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel

{%- if source_url.endswith('.zip') %}
BuildRequires:  unzip
{%- endif %}
BuildRequires:  fdupes
{%- if not has_ext_modules %}
BuildArch:      noarch
{%- endif %}

{%- if provides_extra and provides_extra is not none %}
{%- set provides_extra_comma_separated_list = ','.join(provides_extra)  %}
{%- set have_provides_extra = 1 %}
{%- endif %}

# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
{{ description }}}

%description %_description

%package -n %{python_name}
Summary:        %{summary}

%description -n %{python_name} %_description

{%- if have_provides_extra %}
# For official Fedora packages, review which extras should be actually packaged
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#Extras
%pyproject_extras_subpkg -n %{python_name} {{ provides_extra_comma_separated_list }}
{%- endif %}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires {% if have_provides_extra %}-x {{ provides_extra_comma_separated_list }}{% endif %}


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto


{%- if testsuite or test_suite %}
%if %{with test}
%check
%pyproject_check_import
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


