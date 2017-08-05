Format: 1.0
Source: {{ name }}
Version: {{ version }}
Binary: python-{{ name|lower }}
Maintainer: {{ user_name }}
Architecture: any
Standards-Version: 3.7.1
Build-Depends: debhelper (>= 4.0.0), python-dev{% for req in requires %}, python-{{ req|lower|parenthesize_version }}{% endfor %}{% for req in install_requires %}, python-{{ req|lower|parenthesize_version }}{% endfor %}
{%- if requires or install_requires %}
Depends: {% for req in requires %}python-{{ req|lower|parenthesize_version }}{{ ', ' if not loop.last or install_requires }}{% endfor %}{% for req in install_requires %}python-{{ req|lower|parenthesize_version }}{{ ', ' if not loop.last }}{% endfor %}
{%- endif %}
{%- if extras_require %}
Suggests: {% for reqlist in extras_require.values() %}{% for req in reqlist %}python-{{ req|lower|parenthesize_version }}{{ ', ' if not loop.last }}{%- endfor %}{{ ', ' if not loop.last }}{%- endfor %}
{%- endif %}

