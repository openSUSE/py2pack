%global pypi_name sampleproject
%global python_name python3-%{pypi_name}

%bcond_without test

Name:           python-%{pypi_name}
Version:        3.0.0
Release:        %autorelease
Summary:        A sample Python project

# Check the generated license identifier against Fedora's licensing guidelines.
License:        Copyright (c) 2016 The Python Packaging Authority (PyPA)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
 (FIXME:No SPDX)
URL:            https://github.com/pypa/sampleproject
Source:         https://files.pythonhosted.org/packages/source/s/sampleproject/sampleproject-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(setuptools) >= 43.0.0
BuildRequires:  python3dist(wheel)

%if %{with test}
BuildRequires:  python3dist(coverage)
BuildRequires:  python3dist(peppercorn)
BuildRequires:  python3dist(pytest)
%endif

%global _description %{expand:
A sample Python project}

%description %_description

%package -n %{python_name}
Summary:        %{summary}
Requires:       python3dist(peppercorn)
Suggests:       python3dist(check-manifest)

%description -n %{python_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -L sample

%check
%if %{with test}
# Adjust the test runner and arguments to match the upstream test suite.
%pytest
%endif

%files -n %{python_name} -f %{pyproject_files}
%doc README.md
%license LICENSE.txt
%{_bindir}/sample

%changelog
%autochangelog