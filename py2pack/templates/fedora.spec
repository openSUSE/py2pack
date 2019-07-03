#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#

# Single python3 version in Fedora, python36 or python34 for RHEL
%{!?python3_pkgversion:%global python3_pkgversion 3}

%global with_python3 1
%if 0%{?fedora} > 30
%global with_python2 1
%else
%global with_python2 0

Name:           python-{{ name }}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
Source:         {{ source_url|replace(version, '%{version}') }}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if %{with_python2}
BuildRequires:  python2-devel {%- if requires_python %} = {{ requires_python }} {% endif %}
{%- for req in requires %}
BuildRequires:  python2-{{ req|replace('(','')|replace(')','') }}
Requires:       python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%endif
%if %{with_python3}
BuildRequires:  python%{python3_pkgversion}-devel {%- if requires_python %} = {{ requires_python }} {% endif %}
{%- for req in requires %}
BuildRequires:  python%{python3_pkgversion}-{{ req|replace('(','')|replace(')','') }}
Requires:       python%{python3_pkgversion}-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%endif

%description
{{ description }}

%if %{with_python2}
%package -n python2-{{ name }}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
{%- for req in install_requires %}
BuildRequires:  python2-{{ req|replace('(','')|replace(')','') }}
Requires:       python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- if extras_require %}
%if 0%{fedora} > 0
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endfor %}
%endif
{%- endif %}

%description -n python2-{{ name }}
{{ description }}
%endif # with_python2

%if %{with_python3}
%package -n python%{python3-pkgveraion}-{{ name }}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
{%- for req in install_requires %}
BuildRequires:  python%{python3-pkgversion}-{{ req|replace('(','')|replace(')','') }}
Requires:       python%{python3-pkgversion}-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- if extras_require %}
%if 0%{fedora} > 0
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python%{python3-pkgversion}-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endfor %}
%endif
{%- endif %}

%description -n python%{pyton3-pkgversion}-{{ name }}
{{ description }}
%endif # with_python2

%prep
%setup -q -n {{ name }}-%{version}

%build
{%- if is_extension %}
export CFLAGS="%{optflags}"
{%- endif %}

%if %{with_python2}
%{__python2} setup.py build
%endif

%if %{with_python3}
%{__python3} setup.py build
%endif

%install
%if %{with_python2}
%{__python2} setup.py install --prefix=%{_prefix} --root=%{buildroot}
%endif

%if %{with_python3}
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}
%endif

%clean
rm -rf %{buildroot}

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

