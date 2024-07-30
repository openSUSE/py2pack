%define pypi_name py2pack
%define python_name python3-%{pypi_name}
Name:           python-%{pypi_name}
Version:        0.8.5
Release:        %autorelease
Summary:        Generate distribution packages from PyPI

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        Apache-2.0
URL:            http://github.com/openSUSE/py2pack
Source:         https://files.pythonhosted.org/packages/source/p/py2pack/py2pack-%{version}.tar.gz

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python-devel
%if %{undefined python_module}
%define python_module() python3dist(%1)
%endif
BuildRequires:  %{python_module pbr >= 1.8}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module wheel}
# SECTION test requirements
%if %{with test}
BuildRequires:  %{python_module Jinja2}
BuildRequires:  %{python_module metaextract}
BuildRequires:  %{python_module six}
%endif
# /SECTION
BuildRequires:  fdupes
Requires:       %{python_module Jinja2}
Requires:       %{python_module metaextract}
Requires:       %{python_module setuptools}
Requires:       %{python_module six}
Suggests:       %{python_module typing}
BuildArch:      noarch

# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
Generate distribution packages from PyPI}

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
#
#%python_clone -a %{buildroot}%{_bindir}/py2pack
#
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto
%if %{with test}
%check
%pytest
%endif

%files -n %{python_name} -f %{pyproject_files}

%changelog
%autochangelog

