#
# spec file for package python-py2pack
#
# Copyright (c) 2025 SUSE LLC
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


Name:           python-py2pack
Version:        0.8.5
Release:        0
Summary:        Generate distribution packages from PyPI
License:        Apache-2.0
URL:            http://github.com/openSUSE/py2pack
Source:         https://files.pythonhosted.org/packages/source/p/py2pack/py2pack-%{version}.tar.gz
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module pbr >= 1.8}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module wheel}
# SECTION test requirements
BuildRequires:  %{python_module Jinja2}
BuildRequires:  %{python_module metaextract}
BuildRequires:  %{python_module six}
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
%autosetup -p1 -n py2pack-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
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
%{python_sitelib}/py2pack
%{python_sitelib}/py2pack-%{version}.dist-info

%changelog
