#
# spec file for package python-{{ name|lower }}
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

# norootforbuild

%define mod_name {{ name|lower }}

Name:           python-%{mod_name}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
{%- if name != name|lower %}
Source:         {{ name }}-%{version}{{ ending }}
{%- else %}
Source:         %{mod_name}-%{version}{{ ending }}
{%- endif %}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
{%- for req in requires %}
BuildRequires:  python-{{ req|lower }}
Requires:       python-{{ req|lower }}
{%- endfor %}
%if 0%{?suse_version}
%py_requires
%if %{?suse_version: %{suse_version} > 1110} %{!?suse_version:1}
BuildArch:      noarch
%endif
%endif

%description
{{ description }}

Authors:
--------
    {{ author }} <{{ author_email }}>

%prep
export CFLAGS="%{optflags}"
{%- if name != name|lower %}
%setup -n {{ name }}-%{version}
{%- else %}
%setup -n %{mod_name}-%{version}
{%- endif %}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot} %{?suse_version: --record-rpm=INSTALLED_FILES}

%clean
%{__rm} -rf %{buildroot}

%files %{?suse_version: -f INSTALLED_FILES}
%defattr(-,root,root,-)
%if 0%{!?suse_version:1}
# You may have to add additional files here!
%python_sitelib/%{mod_name}*
%endif

%changelog
