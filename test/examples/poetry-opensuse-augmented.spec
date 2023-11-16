#
# spec file for package python-poetry
#
# Copyright (c) 2023 SUSE LLC
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


Name:           python-poetry
Version:        1.5.1
Release:        0
Summary:        Python dependency management and packaging made easy
License:        MIT
URL:            https://python-poetry.org/
Source:         https://files.pythonhosted.org/packages/source/p/poetry/poetry-%{version}.tar.gz
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module poetry-core >= 1.5.0}
# SECTION test requirements
BuildRequires:  %{python_module build >= 0.10.0}
BuildRequires:  %{python_module cachecontrol >= 0.12.9}
BuildRequires:  %{python_module cleo >= 2.0.0}
BuildRequires:  %{python_module crashtest >= 0.4.1}
BuildRequires:  %{python_module dulwich >= 0.21.2}
BuildRequires:  %{python_module filelock >= 3.8.0}
BuildRequires:  %{python_module html5lib >= 1.0}
BuildRequires:  %{python_module installer >= 0.7.0}
BuildRequires:  %{python_module jsonschema >= 4.10.0}
BuildRequires:  %{python_module keyring >= 23.9.0}
BuildRequires:  %{python_module lockfile >= 0.12.2}
BuildRequires:  %{python_module packaging >= 20.4}
BuildRequires:  %{python_module pexpect >= 4.7.0}
BuildRequires:  %{python_module pkginfo >= 1.9.4}
BuildRequires:  %{python_module platformdirs >= 3.0.0}
BuildRequires:  %{python_module poetry-core == 1.6.1}
BuildRequires:  %{python_module poetry-plugin-export >= 1.4.0}
BuildRequires:  %{python_module pyproject-hooks >= 1.0.0}
BuildRequires:  %{python_module requests >= 2.18}
BuildRequires:  %{python_module requests-toolbelt >= 0.9.1}
BuildRequires:  %{python_module shellingham >= 1.5}
BuildRequires:  %{python_module tomlkit >= 0.11.4}
BuildRequires:  %{python_module trove-classifiers >= 2022.5.19}
BuildRequires:  %{python_module urllib3 >= 1.26.0}
BuildRequires:  %{python_module virtualenv >= 20.22.0}
BuildRequires:  %{python_module cachy}
BuildRequires:  %{python_module deepdiff}
BuildRequires:  %{python_module httpretty}
BuildRequires:  %{python_module pytest}
BuildRequires:  %{python_module pytest-cov}
BuildRequires:  %{python_module pytest-mock}
BuildRequires:  %{python_module pytest-randomly}
BuildRequires:  %{python_module pytest-xdist}
BuildRequires:  %{python_module zipp}
# /SECTION
BuildRequires:  fdupes
Requires:       python-build >= 0.10.0
Requires:       python-cachecontrol >= 0.12.9
Requires:       python-cleo >= 2.0.0
Requires:       python-crashtest >= 0.4.1
Requires:       python-dulwich >= 0.21.2
Requires:       python-filelock >= 3.8.0
Requires:       python-html5lib >= 1.0
Requires:       python-installer >= 0.7.0
Requires:       python-jsonschema >= 4.10.0
Requires:       python-keyring >= 23.9.0
Requires:       python-lockfile >= 0.12.2
Requires:       python-packaging >= 20.4
Requires:       python-pexpect >= 4.7.0
Requires:       python-pkginfo >= 1.9.4
Requires:       python-platformdirs >= 3.0.0
Requires:       python-poetry-core == 1.6.1
Requires:       python-poetry-plugin-export >= 1.4.0
Requires:       python-pyproject-hooks >= 1.0.0
Requires:       python-requests >= 2.18
Requires:       python-requests-toolbelt >= 0.9.1
Requires:       python-shellingham >= 1.5
Requires:       python-tomlkit >= 0.11.4
Requires:       python-trove-classifiers >= 2022.5.19
Requires:       python-urllib3 >= 1.26.0
Requires:       python-virtualenv >= 20.22.0
BuildArch:      noarch
%python_subpackages

%description
# Poetry: Python packaging and dependency management made easy

[![Stable Version](https://img.shields.io/pypi/v/poetry?label=stable)][PyPI Releases]
[![Pre-release Version](https://img.shields.io/github/v/release/python-poetry/poetry?label=pre-release&include_prereleases&sort=semver)][PyPI Releases]
[![Python Versions](https://img.shields.io/pypi/pyversions/poetry)][PyPI]
[![Download Stats](https://img.shields.io/pypi/dm/poetry)](https://pypistats.org/packages/poetry)
[![Discord](https://img.shields.io/discord/487711540787675139?logo=discord)][Discord]

Poetry helps you declare, manage and install dependencies of Python projects,
ensuring you have the right stack everywhere.

![Poetry Install](https://raw.githubusercontent.com/python-poetry/poetry/master/assets/install.gif)

Poetry replaces `setup.py`, `requirements.txt`, `setup.cfg`, `MANIFEST.in` and `Pipfile` with a simple `pyproject.toml`
based project format.

```toml
[tool.poetry]
name = "my-package"
version = "0.1.0"
description = "The description of the package"

license = "MIT"

authors = [
    "Sébastien Eustace <sebastien@eustace.io>"
]

repository = "https://github.com/python-poetry/poetry"
homepage = "https://python-poetry.org"

# README file(s) are used as the package description
readme = ["README.md", "LICENSE"]

# Keywords (translated to tags on the package index)
keywords = ["packaging", "poetry"]

[tool.poetry.dependencies]
# Compatible Python versions
python = ">=3.8"
# Standard dependency with semver constraints
aiohttp = "^3.8.1"
# Dependency with extras
requests = { version = "^2.28", extras = ["security"] }
# Version-specific dependencies with prereleases allowed
tomli = { version = "^2.0.1", python = "<3.11", allow-prereleases = true }
# Git dependencies
cleo = { git = "https://github.com/python-poetry/cleo.git", branch = "master" }
# Optional dependencies (installed by extras)
pendulum = { version = "^2.1.2", optional = true }

# Dependency groups are supported for organizing your dependencies
[tool.poetry.group.dev.dependencies]
pytest = "^7.1.2"
pytest-cov = "^3.0"

# ...and can be installed only when explicitly requested
[tool.poetry.group.docs]
optional = true
[tool.poetry.group.docs.dependencies]
Sphinx = "^5.1.1"

# Python-style entrypoints and scripts are easily expressed
[tool.poetry.scripts]
my-script = "my_package:main"
```

## Installation

Poetry supports multiple installation methods, including a simple script found at [install.python-poetry.org]. For full
installation instructions, including advanced usage of the script, alternate install methods, and CI best practices, see
the full [installation documentation].

## Documentation

[Documentation] for the current version of Poetry (as well as the development branch and recently out of support
versions) is available from the [official website].

## Contribute

Poetry is a large, complex project always in need of contributors. For those new to the project, a list of
[suggested issues] to work on in Poetry and poetry-core is available. The full [contributing documentation] also
provides helpful guidance.

## Resources

* [Releases][PyPI Releases]
* [Official Website]
* [Documentation]
* [Issue Tracker]
* [Discord]

  [PyPI]: https://pypi.org/project/poetry/
  [PyPI Releases]: https://pypi.org/project/poetry/#history
  [Official Website]: https://python-poetry.org
  [Documentation]: https://python-poetry.org/docs/
  [Issue Tracker]: https://github.com/python-poetry/poetry/issues
  [Suggested Issues]: https://github.com/python-poetry/poetry/contribute
  [Contributing Documentation]: https://python-poetry.org/docs/contributing
  [Discord]: https://discord.com/invite/awxPgve
  [install.python-poetry.org]: https://install.python-poetry.org
  [Installation Documentation]: https://python-poetry.org/docs/#installation

## Related Projects

* [poetry-core](https://github.com/python-poetry/poetry-core): PEP 517 build-system for Poetry projects, and
dependency-free core functionality of the Poetry frontend
* [poetry-plugin-export](https://github.com/python-poetry/poetry-plugin-export): Export Poetry projects/lock files to
foreign formats like requirements.txt
* [poetry-plugin-bundle](https://github.com/python-poetry/poetry-plugin-bundle): Install Poetry projects/lock files to
external formats like virtual environments
* [install.python-poetry.org](https://github.com/python-poetry/install.python-poetry.org): The official Poetry
installation script
* [website](https://github.com/python-poetry/website): The official Poetry website and blog



%prep
%autosetup -p1 -n poetry-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%python_clone -a %{buildroot}%{_bindir}/poetry
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%check
CHOOSE: %pytest OR %pyunittest -v OR CUSTOM

%post
%python_install_alternative poetry

%postun
%python_uninstall_alternative poetry

%files %{python_files}
%doc README.md
%license LICENSE
%python_alternative %{_bindir}/poetry
%{python_sitelib}/poetry
%{python_sitelib}/poetry-%{version}.dist-info

%changelog
