import sys
from pathlib import Path
sys.path.append(str(Path(".").resolve()))

project = 'rivtlib.net'
copyright = '2023 StructureLabs'
author = 'rholland'
release = '0.1'

myst_heading_anchors = 3

myst_enable_extensions = ['substitution', 'deflist', 'attrs_block',
                          'html_image', 'amsmath']

extensions = ['myst_parser', 'sphinx.ext.githubpages',
              "sphinxcontrib.jquery", 'sphinx_copybutton', 'sphinx_favicon']
html_theme = 'pydata_sphinx_theme'
html_sidebars = {"**": []}
source_suffix = ['.rst', '.md']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_static_path = ['_static', '_static/img/']
html_context = {"default_mode": "auto"}
html_logo = "_static/img/rivtpy64.png"
html_theme_options = {
    "show_nav_level": 2,
    "show_toc_level": 3,
    "navigation_depth": 3,
    "footer_start": ["copyright"],
    "footer_end": [],
    "logo": {
        "image_dark": "_static/img/rivtpy64.png",
        "image_light": "_static/img/rivtpy64.png",
    }
}

favicons = [
    {"href": "favicon-32x32.png"},
    {"href": "favicon-16x16.png"},
]

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
