%define mod_name {{ name|lower }}

Name:           python-%{mod_name}
Version:        {{ version }}
Release:        %mkrel 1
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Python
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  python-devel
{%- for req in requires %}
BuildRequires:  {{ req|rpm_format_requires("python-")|lower }}
Requires:       {{ req|rpm_format_requires("python-")|lower }}
{%- endfor %}
{%- for req in install_requires %}
BuildRequires:  {{ req|rpm_format_requires("python-")|lower }}
Requires:       {{ req|rpm_format_requires("python-")|lower }}
{%- endfor %}
{%- if extras_require %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       {{ req|rpm_format_requires("python-")|lower }}
{%- endfor %}
{%- endfor %}
{%- endif %}

%description
{{ summary }}


%prep
{%- if name != name|lower %}
%setup -q -n {{ name }}-%{version}
{%- else %}
%setup -q -n %{mod_name}-%{version}
{%- endif %}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files -f
%defattr(-,root,root)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- if scripts %}
{%- for script in scripts %}
%{_bindir}/{{ script }}
{%- endfor %}
{%- endif %}
%{python_sitelib}/*

