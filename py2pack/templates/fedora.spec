#
# spec file for package python-{{ name }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#

# Fedora and RHEL split python2 and python3
# Older RHEL does not include python3 by default
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%else
%global with_python3 0
%endif

# Fedora > 28 no longer publishes python2 by default
%if 0%{?fedora} > 28
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

# Common SRPM package
Name:           python-{{ name }}
Version:        {{ version }}
Release:        0.1
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
Source:         {{ source_url|replace(version, '%{version}') }}
{%- if not has_ext_modules %}
BuildArch:      noarch
{%- endif %}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?with_python2}
BuildRequires:  python2-devel {%- if requires_python %} = {{ requires_python }} {% endif %}
{%- for req in requires %}
BuildRequires:  python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- for req in install_requires %}
BuildRequires:  python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%endif # with_python2
%if 0%{?with_python3}
BuildRequires:  python3-devel {%- if requires_python %} = {{ requires_python }} {% endif %}
{%- for req in requires %}
BuildRequires:  python3-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- for req in install_requires %}
BuildRequires:  python3-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%endif # with_python3

%if 0%{?with_python2}
%package -n python2-{{ name }}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
{%- for req in requires %}
Requires:       python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- for req in install_requires %}
Requires:       python2-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%if 0%{with_dnf}
{%- if extras_require %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python20{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endfor %}
{%- endif %}
%endif # with_dnf
%{?python_provide:%python_provide python2-%{srcname}}
%endif # with_python2

%if 0%{?with_python3}
%package -n python3-{{ name }}
Version:        {{ version }}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
{%- for req in requires %}
Requires:       python3-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- for req in install_requires %}
Requires:       python3-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
%if 0%{with_dnf}
{%- if extras_require %}
{%- for reqlist in extras_require.values() %}
{%- for req in reqlist %}
Suggests:       python3-{{ req|replace('(','')|replace(')','') }}
{%- endfor %}
{%- endfor %}
{%- endif %}
%endif # with_dnf
%{?python_provide:%python_provide python2-%{srcname}}
%endif # with_python3

%description
{{ description }}

%if 0%{?with_python2}
%description -n python2-{{ name }}
{{ description }}
%endif # with_python2

%if 0%{?with_python3}
%description -n python3-{{ name }}
{{ description }}
%endif # with_python3

%prep
%setup -q -n {{ name }}-%{version}

%build
{%- if is_extension %}
export CFLAGS="%{optflags}"
{%- endif %}
%if 0%{?with_python2}
%py2_build
%endif # with_python2
%if 0%{?with_python3}
%py2_build
%endif # with_python3

%install
%if 0%{?with_python2}
%py2_install
{%- for script in scripts %}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/${script} $RPM_BUILD_ROOT%{_bindir}/${script}2
%{__ln_s} ${script}2 $RPM_BUILD_ROOT%{_bindir}/${script}
{%- endfor %}
%endif # with_python2
%if 0%{?with_python3}
%py3_install
{%- for script in scripts %}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/${script} $RPM_BUILD_ROOT%{_bindir}/${script}3
%{__ln_s} ${script}3 $RPM_BUILD_ROOT%{_bindir}/${script}
{%- endfor %}
%endif # with_python3

%clean
rm -rf %{buildroot}

%if 0%{with_python2}
%files -n python2-{{ name }}
%defattr(-,root,root,-)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- for script in scripts %}
%{_bindir}/{{ script }}2
{%- endfor %}
{%- if is_extension %}
%if ! 0%{with_python3}
# Symlinks for binaries renamed to ${script}2, only if with_python3 is not enabled
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

%if 0%{with_python3}
%files -n python3-{{ name }}
%defattr(-,root,root,-)
{%- if doc_files %}
%doc {{ doc_files|join(" ") }}
{%- endif %}
{%- for script in scripts %}
%{_bindir}/{{ script }}3
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
