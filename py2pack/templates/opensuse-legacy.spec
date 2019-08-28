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

# Please submit bugfixes or comments via https://bugs.opensuse.org/


Name:           python-{{ name }}
Version:        {{ version }}
Release:        0
Summary:        {{ summary_no_ending_dot|default(summary, true) }}
License:        {{ license }}
URL:            {{ home_page }}
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRequires:  python-setuptools
{%- if install_requires and install_requires is not none %}
{%- for req in install_requires|sort %}
BuildRequires:  python-{{ req }}
{%- endfor %}
{%- endif %}
{%- if tests_require and tests_require is not none %}
# test requirements
{%- for req in tests_require|sort %}
BuildRequires:  python-{{ req }}
{%- endfor %}
{%- endif %}
{%- if source_url.endswith('.zip') %}
BuildRequires:  unzip
{%- endif %}
{%- if install_requires and install_requires is not none %}
{%- for req in install_requires|sort %}
Requires:       python-{{ req }}
{%- endfor %}
{%- endif %}
{%- if extras_require and extras_require is not none %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python-{{ req }}
{%- endfor %}
{%- endfor %}
{%- endif %}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
{%- if not has_ext_modules %}
BuildArch:      noarch
{%- endif %}

%description
{{ description }}

%prep
%setup -q -n {{ name }}-%{version}

%build
{% if has_ext_modules %}CFLAGS="%{optflags}" {% endif %}python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

{%- if testsuite or test_suite %}
%check
python setup.py test
{%- endif %}

%files
%defattr(-,root,root,-)
{%- if doc_files and doc_files is not none %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- if license_files and license_files is not none %}
%license {{ license_files|join(" ") }}
{%- endif %}
{%- if scripts and scripts is not none %}
{%- for script in scripts %}
%{_bindir}/{{ script|basename }}
{%- endfor %}
{%- endif %}
{%- if console_scripts and console_scripts is not none %}
{%- for script in console_scripts %}
%{_bindir}/{{ script }}
{%- endfor %}
{%- endif %}
{%- if has_ext_modules %}
%{python_sitearch}/*
{%- else %}
%{python_sitelib}/*
{%- endif %}
{%- if data_files and data_files is not none %}
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
{%- endif %}

%changelog

