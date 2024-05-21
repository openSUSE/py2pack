%define pypi_name sampleproject
%define python_name python3-%{pypi_name}
Name:           python-%{pypi_name}
Version:        3.0.0
Release:        %autorelease
Summary:        A sample Python project

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
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

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python-devel
%if %{undefined python_module}
%define python_module() python3dist(%1)
%endif
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools >= 43.0.0}
BuildRequires:  %{python_module wheel}
# SECTION test requirements
%if %{with test}
BuildRequires:  %{python_module peppercorn}
BuildRequires:  %{python_module coverage}
%endif
# /SECTION
BuildRequires:  fdupes
Requires:       %{python_module peppercorn}
Suggests:       %{python_module check-manifest}
BuildArch:      noarch

# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
A sample Python project}

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
#%python_clone -a %{buildroot}%{_bindir}/sample
#
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto

%files -n %{python_name} -f %{pyproject_files}

%changelog
%autochangelog

