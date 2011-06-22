#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} {{ user_name }}.
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

%description
{{ description }}

%prep
%setup -q -n {{ name }}-%{version}

%build
export CFLAGS="%{optflags}"
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
# You may have to add additional files here (documentation and binaries mostly)
%{python_sitelib}/*

%changelog

