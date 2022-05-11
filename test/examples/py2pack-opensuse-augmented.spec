#
# spec file for package python-py2pack
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


%{?!python_module:%define python_module() python-%{**} python3-%{**}}
Name:           python-py2pack
Version:        0.8.5
Release:        0
Summary:        Generate distribution packages from PyPI
License:        Apache-2.0
URL:            http://github.com/openSUSE/py2pack
Source:         https://files.pythonhosted.org/packages/source/p/py2pack/py2pack-%{version}.tar.gz
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module pbr >= 1.8}
# SECTION test requirements
BuildRequires:  %{python_module Jinja2}
BuildRequires:  %{python_module metaextract}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module six}
BuildRequires:  %{python_module coverage}
BuildRequires:  %{python_module ddt}
BuildRequires:  %{python_module flake8}
BuildRequires:  %{python_module pytest}
BuildRequires:  %{python_module Sphinx >= 1.2.1}
BuildRequires:  %{python_module sphinxcontrib.programoutput}
# /SECTION
BuildRequires:  fdupes
Requires:       python-Jinja2
Requires:       python-metaextract
Requires:       python-setuptools
Requires:       python-six
Suggests:       python-typing
BuildArch:      noarch
%python_subpackages

%description
Generate distribution packages from PyPI

%prep
%setup -q -n py2pack-%{version}

%build
%python_build

%install
%python_install
%python_clone -a %{buildroot}%{_bindir}/py2pack
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%check
CHOOSE: %pytest OR %pyunittest -v OR CUSTOM

%post
%python_install_alternative py2pack

%postun
%python_uninstall_alternative py2pack

%files %{python_files}
%doc AUTHORS ChangeLog README.rst
%license LICENSE
%python_alternative %{_bindir}/py2pack
%{python_sitelib}/*

%changelog
