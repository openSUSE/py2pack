#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#

%define mod_name {{ name }}

Name:           python-%{mod_name}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
Source:         {{ file_name }}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
{%- for req in requires %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
Requires:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}

%description
{{ description }}

%prep
%setup -q -n %{mod_name}-%{version}

%build
python setup.py build

%install
export CFLAGS="%{optflags}"
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
# You may have to add additional files here (documentation and binaries mostly)
%python_sitelib/1

%changelog

