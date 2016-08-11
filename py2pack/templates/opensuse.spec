#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} SUSE LINUX GmbH, Nuernberg, Germany.
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
BuildRequires:  python-setuptools
{%- for req in install_requires|sort %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- if tests_require %}
# test requirements
{%- for req in tests_require|sort %}
BuildRequires:  python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endif %}
{%- if source_url.endswith('.zip') %}
BuildRequires:  unzip
{%- endif %}
{%- for req in install_requires|sort %}
Requires:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- if extras_require %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endfor %}
{%- endif %}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

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
python setup.py test
{%- endif %}

%files
%defattr(-,root,root,-)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- for script in scripts %}
%{_bindir}/{{ script|basename }}
{%- endfor %}
{%- for script in console_scripts %}
%{_bindir}/{{ script }}
{%- endfor %}
{%- if is_extension %}
%{python_sitearch}/*
{%- else %}
%{python_sitelib}/*
{%- endif %}
{%- for dir, files in data_files %}
{%- set dir = dir |
    replace('/usr/share/doc/'~name, '%doc %{_defaultdocdir}/%{name}', 1) |
    replace('/usr/share/man/', '%doc %{_mandir}/', 1) |
    replace('/usr/share/', '%{_datadir}/', 1) |
    replace('/usr/', '%{_prefix}/', 1) %}
%dir {{ dir }}
{%- for file in files %}
{{ dir }}/{{file|basename }}
{%- endfor %}
{%- endfor %}

%changelog
