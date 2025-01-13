__USER__%define mod_name poetry

Name:           python-%{mod_name}
Version:        1.5.1
Release:        %mkrel 1
Url:            https://python-poetry.org/
Summary:        Python dependency management and packaging made easy.
License:        MIT
Group:          Development/Python
Source:         https://files.pythonhosted.org/packages/source/p/poetry/poetry-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  python-devel

%description
Python dependency management and packaging made easy.


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
