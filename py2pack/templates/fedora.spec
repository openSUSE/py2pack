#
# spec file for package python-{{ name }}
#

Name:           python-{{ name}}
Version:        {{ version}}
Release:        0
Url:            {{ home_page }}
Summary:        {{ summary }}
License:        {{ license }}
Group:          Development/Languages/Python
%define mod_name {{ name }}
Source:         %{mod_name}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
{% for req in requirements %}
BuildRequires:  {{ req }}
Requires:       {{ req }}
{% endfor %}

%py_requires

%description
{{ summary }}

Authors:
--------
    {{ author}} <{{ author_email }}>

%prep
%setup -n %{mod_name}-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT --record-rpm=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root,-)

%changelog

