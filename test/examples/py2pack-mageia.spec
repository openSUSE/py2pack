%define mod_name py2pack

Name:           python-%{mod_name}
Version:        0.8.5
Release:        %mkrel 1
Url:            http://github.com/openSUSE/py2pack
Summary:        Generate distribution packages from PyPI
License:        Apache-2.0
Group:          Development/Python
Source:         https://files.pythonhosted.org/packages/source/p/py2pack/py2pack-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  python-devel

%description
Generate distribution packages from PyPI


%prep
%setup -q -n %{mod_name}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files -f
%defattr(-,root,root)
%{python_sitelib}/*
