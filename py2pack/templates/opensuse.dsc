Format: 1.0
Source: {{ name }}
Version: {{ version }}
Binary: python-{{ name|lower }}
Maintainer: {{ user_name }}
Architecture: any
Standards-Version: 3.7.1
Build-Depends: debhelper (>= 4.0.0), python-dev{% for req in requires %}, python-{{ req|lower }}{% endfor %}
