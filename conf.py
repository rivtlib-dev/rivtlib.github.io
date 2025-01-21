import sys
from pathlib import Path
sys.path.append(str(Path(".").resolve()))

project = 'rivtlib.net'
copyright = '2023 StructureLabs'
author = 'rholland'
release = '0.1'

extensions = ['sphinx.ext.githubpages',
              "sphinxcontrib.jquery", 'sphinx_copybutton',
              'sphinx_favicon', 'sphinx.ext.duration',
              'sphinx.ext.doctest', 'sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = ['.rst']

html_theme = 'pydata_sphinx_theme'
html_context = {"default_mode": "light"}
html_sidebars = {"**": []}
html_static_path = ['_static', '_static/img/']
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
