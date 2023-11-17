#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#

Name:           python-{{ name }}
Version:        {{ version }}
Release:        0
Summary:        {{ summary }}
License:        {{ license }}
URL:            {{ home_page }}
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel {%- if requires_python %} {{ requires_python }} {% endif %}
{%- for req in requires %}
BuildRequires:  {{ req|rpm_format_requires("python-") }}
Requires:       {{ req|rpm_format_requires }}
{%- endfor %}
{%- for req in install_requires %}
BuildRequires:  {{ req|rpm_format_requires("python-") }}
Requires:       {{ req|rpm_format_requires("python-") }}
{%- endfor %}
{%- if extras_require %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       {{ req|rpm_format_requires("python-") }}
{%- endfor %}
{%- endfor %}
{%- endif %}

%description
{{ description }}

%prep
%setup -q -n {{ name }}-%{version}

%build
{%- if is_extension %}
export CFLAGS="%{optflags}"
{%- endif %}
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- for script in scripts|default([], true) %}
%{_bindir}/{{ script }}
{%- endfor %}
%{python_sitelib}/*

%changelog

