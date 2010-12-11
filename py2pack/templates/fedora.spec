#
# spec file for package python-{{ name|lower }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#

Name:           python-{{ name|lower }}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
%define mod_name {{ name }}
Source:         %{mod_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
{%- for req in requires %}
BuildRequires:  python-{{ req|lower }}
Requires:       pyhton-{{ req|lower }}
{%- endfor %}

%description
{{ summary }}

Authors:
--------
    {{ author }} <{{ author_email }}>

%prep
export CFLAGS="%{optflags}"
%setup -n %{mod_name}-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
# You may have to add additional files here!
/usr/lib/python2.6/site-packages/%{mod_name}*

%changelog

