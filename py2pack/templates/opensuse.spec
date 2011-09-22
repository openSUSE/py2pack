#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           python-{{ name }}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel {%- if requires_python %} = {{ requires_python }} {% endif %}
{%- for req in requires %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
Requires:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- for req in install_requires %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
Requires:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%if 0%{?suse_version}
%py_requires
%if 0%{?suse_version} > 1110
BuildArch:      noarch
%endif
%endif
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description
{{ description }}

%prep
%setup -q -n {{ name }}-%{version}

%build
CFLAGS="%{optflags}" python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
# You may have to add additional files here (documentation and binaries mostly)
%{python_sitelib}/*

%changelog
