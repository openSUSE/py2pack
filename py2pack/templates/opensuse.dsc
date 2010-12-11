#
# dsc file for package python-{{ name|lower }}
#
# Copyright (c) {{ year }} {{ user_name }}.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/

Format: 1.0
Source: {{ name }}-{{ version }}.tar.gz
Version: {{ version }}
Binary: python-{{ name|lower }}
Maintainer: {{ user_name }}
Architecture: any
Standards-Version: 3.7.1
Build-Depends: debhelper (>= 4.0.0), python-dev{% for req in requires %}, python-{{ req|lower }}{% endfor %}
