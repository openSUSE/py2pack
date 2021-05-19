#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} SUSE LLC
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
#


%{?!python_module:%define python_module() python-%{**} python3-%{**}}
Name:           python-{{ name }}
Version:        {{ version }}
Release:        0
Summary:        {{ summary_no_ending_dot|default(summary, true) }}
License:        {{ license }}
URL:            {{ home_page }}
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module setuptools}
{%- if setup_requires and setup_requires is not none %}
{%- for req in setup_requires|sort %}
BuildRequires:  %{python_module {{ req }}}
{%- endfor %}
{%- endif %}
{%- if (install_requires and install_requires is not none) or (tests_require and tests_require is not none) %}
# SECTION test requirements
{%- if install_requires and install_requires is not none %}
{%- for req in install_requires|sort %}
BuildRequires:  %{python_module {{ req }}}
{%- endfor %}
{%- endif %}
{%- if tests_require and tests_require is not none %}
{%- for req in tests_require|sort %}
BuildRequires:  %{python_module {{ req }}}
{%- endfor %}
{%- endif %}
# /SECTION
{%- endif %}
{%- if source_url.endswith('.zip') %}
BuildRequires:  unzip
{%- endif %}
BuildRequires:  fdupes
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
{%- if not has_ext_modules %}
BuildArch:      noarch
{%- endif %}
%python_subpackages

%description
{{ description }}

%prep
%setup -q -n {{ name }}-%{version}

%build
{%- if has_ext_modules %}
export CFLAGS="%{optflags}"
{%- endif %}
%python_build

%install
%python_install
{%- set scripts_or_console_scripts = (
            (scripts|map('basename')|list if scripts and scripts is not none else []) +
            (console_scripts if console_scripts and console_scripts is not none else [])) %}
{%- for script in scripts_or_console_scripts %}
%python_clone -a %{buildroot}%{_bindir}/{{ script }}
{%- endfor %}
{%- if has_ext_modules %}
%python_expand %fdupes %{buildroot}%{$python_sitearch}
{%- else %}
%python_expand %fdupes %{buildroot}%{$python_sitelib}
{%- endif %}

{%- if testsuite or test_suite %}

%check
{%- if has_ext_modules %}
CHOOSE: %pytest_arch OR %pyunittest_arch -v OR CUSTOM
{%- else %}
CHOOSE: %pytest OR %pyunittest -v OR CUSTOM
{%- endif %}
{%- endif %}

{%- if scripts_or_console_scripts %}

%post
%python_install_alternative {{ scripts_or_console_scripts|join(" ") }}

%postun
%python_uninstall_alternative {{ scripts_or_console_scripts|first }}
{%- endif %}

%files %{python_files}
{%- if doc_files and doc_files is not none %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- if license_files and license_files is not none %}
%license {{ license_files|join(" ") }}
{%- endif %}
{%- for script in scripts_or_console_scripts %}
%python_alternative %{_bindir}/{{ script }}
{%- endfor %}
{%- if has_ext_modules %}
%{python_sitearch}/*
{%- else %}
%{python_sitelib}/*
{%- endif %}
{%- if data_files and data_files is not none %}
{%- for dir, files in data_files %}
{%- set dir = dir |
    replace('/usr/share/doc/'~name, '%doc %{_defaultdocdir}/%{python_prefix}-{{ name }}', 1) |
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

