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
Source:         

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python-devel
BuildRequires:  fdupes
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


%generate_buildrequires
%pyproject_buildrequires 


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto
%if %{with test}
%check
%pyproject_check_import
%pytest
%endif


%files -n %{python_name} -f %{pyproject_files}


%changelog
%autochangelog

