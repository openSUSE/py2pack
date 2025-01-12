Name:           python-setuptools-scm
Version:        8.1.0
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        the blessed package to manage your versions by scm tags

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        MIT
URL:            https://pypi.org/project/setuptools-scm/
Source:         %{pypi_source setuptools_scm}

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'setuptools-scm' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-setuptools-scm
Summary:        %{summary}

%description -n python3-setuptools-scm %_description

# For official Fedora packages, review which extras should be actually packaged
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#Extras
%pyproject_extras_subpkg -n python3-setuptools-scm docs,rich,test


%prep
%autosetup -p1 -n setuptools_scm-%{version}


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires -x docs,rich,test


%build
%pyproject_wheel


%install
%pyproject_install
# Add top-level Python module names here as arguments, you can use globs
%pyproject_save_files -l ...


%check
%pyproject_check_import


%files -n python3-setuptools-scm -f %{pyproject_files}


%changelog
%autochangelog