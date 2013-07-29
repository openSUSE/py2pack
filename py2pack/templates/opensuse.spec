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

# Please submit bugfixes or comments via http://bugs.opensuse.org/


Name:           python-{{ name }}
Version:        {{ version }}
Release:        0
License:        {{ license }}
Summary:        {{ summary_no_ending_dot|default(summary, true) }}
Url:            {{ home_page }}
Group:          Development/Languages/Python
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRequires:  python-devel {%- if requires_python %} = {{ requires_python }} {% endif %}
{%- for req in requires %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
Requires:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- for req in install_requires %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
Requires:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- if source_url.endswith('.zip') %}
BuildRequires:  unzip
{%- endif %}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version} && 0%{?suse_version} <= 1110
{%- if is_extension %}
%{!?python_sitearch: %global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
{%- else %}
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
{%- endif %}
%else
BuildArch:      noarch
%endif

%description
{{ description }}

%prep
%setup -q -n {{ name }}-%{version}

%build
{% if is_extension %}CFLAGS="%{optflags}" {% endif %}python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

{%- if testsuite or test_suite %}

%check
  {%- if test_suite %}
python setup.py test
  {%- else %}
nosetests
  {%- endif %}
{%- endif %}

%files
%defattr(-,root,root,-)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- for script in scripts %}
%{_bindir}/{{ script }}
{%- endfor %}
%{python_sitelib}/*

%changelog
