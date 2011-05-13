%define mod_name {{ name|lower }}

Name:           python-%{mod_name}
Version:        {{ version }}
Release:        %mkrel 1
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Python
{%- if name != name|lower %}
Source:         {{ name }}-%{version}{{ ending }}
{%- else %}
Source:         %{mod_name}-%{version}{{ ending }}
{%- endif %}
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  python-devel
{%- for req in requires %}
BuildRequires:  python-{{ req|lower }}
Requires:       pyhton-{{ req|lower }}
{%- endfor %}

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
%{__python} setup.py install -O1 --skip-build  --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files -f
%defattr(-,root,root)
%{python_sitelib}/*

