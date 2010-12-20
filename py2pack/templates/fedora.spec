#
# spec file for package python-{{ name|lower }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#

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
Requires:       pyhton-{{ req|lower }}
{%- endfor %}

%description
{{ summary }}

Authors:
--------
    {{ author }} <{{ author_email }}>

%prep
{%- if name != name|lower %}
%setup -n {{ name }}-%{version}
{%- else %}
%setup -n %{mod_name}-%{version}
{%- endif %}

%build
export CFLAGS="%{optflags}"
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
# You may have to add additional files here!
%python_sitelib/%{mod_name}*

%changelog

