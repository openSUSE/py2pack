%global pypi_name py2pack
%global python_name python3-%{pypi_name}

%bcond_without test

Name:           python-%{pypi_name}
Version:        0.8.5
Release:        %autorelease
Summary:        Generate distribution packages from PyPI

# Check the generated license identifier against Fedora's licensing guidelines.
License:        Apache-2.0
URL:            http://github.com/openSUSE/py2pack
Source:         https://files.pythonhosted.org/packages/source/p/py2pack/py2pack-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(pbr) >= 1.8
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)

%if %{with test}
BuildRequires:  python3dist(jinja2)
BuildRequires:  python3dist(metaextract)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(six)
%endif

%global _description %{expand:
Generate distribution packages from PyPI}

%description %_description

%package -n %{python_name}
Summary:        %{summary}
Requires:       python3dist(jinja2)
Requires:       python3dist(metaextract)
Requires:       python3dist(setuptools)
Requires:       python3dist(six)
Suggests:       python3dist(typing)

%description -n %{python_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -L py2pack

%check
%if %{with test}
# Adjust the test runner and arguments to match the upstream test suite.
%pytest
%endif

%files -n %{python_name} -f %{pyproject_files}
%doc AUTHORS ChangeLog README.rst
%license LICENSE
%{_bindir}/py2pack

%changelog
%autochangelog