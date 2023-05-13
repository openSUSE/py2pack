#
# spec file for package python-sampleproject
#
# Copyright (c) __YEAR__ SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           python-sampleproject
Version:        3.0.0
Release:        0
Summary:        A sample Python project
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
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools >= 43.0.0}
BuildRequires:  %{python_module wheel}
# SECTION test requirements
BuildRequires:  %{python_module peppercorn}
BuildRequires:  %{python_module coverage}
# /SECTION
BuildRequires:  fdupes
Requires:       python-peppercorn
Suggests:       python-check-manifest
BuildArch:      noarch
%python_subpackages

%description
A sample Python project

%prep
%autosetup -p1 -n sampleproject-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%python_clone -a %{buildroot}%{_bindir}/sample
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%post
%python_install_alternative sample

%postun
%python_uninstall_alternative sample

%files %{python_files}
%doc README.md
%license LICENSE.txt
%python_alternative %{_bindir}/sample
%{python_sitelib}/sampleproject
%{python_sitelib}/sampleproject-%{version}.dist-info

%changelog
