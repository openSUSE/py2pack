#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#

# python3_pkgversion macro for EPEL in older RHEL
%{!?python3_pkgversion:%global python3_pkgversion 3}

# Fedora and RHEL split python2 and python3
# Older RHEL requires EPEL and python34 or python36
%global with_python3 1

# Fedora >= 38 no longer publishes python2 by default
%if 0%{?fedora} >= 30
%global with_python2 0
%else
%global with_python2 1
%endif

# Older RHEL does not use dnf, does not support "Suggests"
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_dnf 1
%else
%global with_dnf 0
%endif

%global pypi_name {{ name }}

# Descriptions can get long and clutter .spec file
%global common_description %{expand:
{{ description }}
}

# Common SRPM package
Name:           python-%{pypi_name}
Version:        {{ version }}
Release:        0%{?dist}
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
# Stop using py2pack macros, use local macros published by Fedora
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
{%- if not has_ext_modules %}
BuildArch:      noarch
{%- endif %}

%description
{{ description }}

%if %{with_python2}
%package -n python2-%{pypi_name}
Version:        {{ version }}
Release:        0%{?dist}
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# requires stanza of py2pack
{%- for req in requires %}
BuildRequires:  python2-{{ req|replace('(','')|replace(')','') }}
Requires:       python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
# install_requires stanza of py2pack
{%- for req in install_requires %}
BuildRequires:  python2-{{ req|replace('(','')|replace(')','') }}
Requires:       python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%if %{with_dnf}
{%- if extras_require %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endfor %}
{%- endif %}
%endif # with_dnf
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
{{ description }}

%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Version:        {{ version }}
Release:        0%{?dist}
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}

# requires stanza of py2pack
{%- for req in requires %}
BuildRequires:  python%{python3_pkgversion}-{{ req|replace('(','')|replace(')','') }}
Requires:       python%{python3_pkgversion}-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
# install_requires stanza of py2pack
{%- for req in install_requires %}
BuildRequires:  python%{python3_pkgversion}-{{ req|replace('(','')|replace(')','') }}
Requires:       python%{python3_pkgversion}-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%if %{with_dnf}
{%- if extras_require %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python%{python3_pkgversion}-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endfor %}
{%- endif %}
%endif # with_dnf
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
{{ description }}

%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}

%build
{%- if is_extension %}
export CFLAGS="%{optflags}"
{%- endif %}
%if %{with_python2}
%py2_build
%endif # with_python2

%if %{with_python3}
%py3_build
%endif # with_python3

%install
%if %{with_python2}
%py2_install
{%- if scripts %}
{%- for script in scripts %}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{{ script }} $RPM_BUILD_ROOT%{_bindir}/{{ script }}-%{python2_version}
{%- endfor %}

%if ! %{with_python3}
{%- for script in scripts %}
%{__ln_s} {{ script }}-%{python2_version} $RPM_BUILD_ROOT%{_bindir}/{{ script }}
{%- endfor %}
%endif # ! with_python3
{%- endif %}
%endif # with_python2

%if %{with_python3}
%py3_install
{%- for script in scripts %}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{{ script }} $RPM_BUILD_ROOT%{_bindir}/{{ script }}-%{python3_version}
%{__ln_s} {{ script }}-%{python3_version} $RPM_BUILD_ROOT%{_bindir}/{{ script }}
{%- endfor %}
%endif # with_python3

%clean
rm -rf %{buildroot}

%if %{with_python2}
%files -n python2-%{pypi_name}
%defattr(-,root,root,-)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- for script in scripts %}
%{_bindir}/{{ script }}-%{python2_version}
{%- endfor %}
{%- if is_extension %}

%if ! %{with_python3}
# Symlinks for binaries to script-2, only if with_python3 is not enabled
{%- for script in scripts %}
%{_bindir}/{{ script }}
{%- endfor %}
%endif # with_python3
%{python2_archlib}/*
{%- endif %}
{%- if not is_extension %}
%{python2_sitelib}/*
{%- endif %}
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%defattr(-,root,root,-)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- for script in scripts %}
%{_bindir}/{{ script }}-%{python3_version}
{%- endfor %}
{%- for script in scripts %}
%{_bindir}/{{ script }}
{%- endfor %}
{%- if is_extension %}
%{python3_archlib}/*
{%- endif %}
{%- if not is_extension %}
%{python3_sitelib}/*
{%- endif %}
%endif # with_python3

%changelog
