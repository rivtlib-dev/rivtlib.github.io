import sys
from pathlib import Path
sys.path.append(str(Path(".").resolve()))

project = 'rivtlib.dev'
copyright = '2023 StructureLabs'
author = 'rholland'
release = '0.1'

extensions = ['sphinx.ext.githubpages','sphinx_togglebutton',
              "sphinxcontrib.jquery", 'sphinx_copybutton',
              'sphinx_favicon', 'sphinx.ext.duration',
              'sphinx.ext.doctest', 'sphinx.ext.autodoc',
              'sphinx_design', 'sphinx.ext.autosummary', 
              'sphinx.ext.viewcode',]

templates_path = ['_static/templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = ['.rst', '*.py']
master_doc = 'index'
locale_dirs = ['_locale'] 
autosummary_generate = True
toc_object_entries_show_parents = "all"

html_theme = 'pydata_sphinx_theme'
html_show_sourcelink = False
html_context = {"default_mode": "dark"}
html_sidebars = {"**": ["sidebar-nav-bs.html"]}
html_static_path = ['_static', '_static/img']
html_css_files = ['css/custom.css',]
html_theme_options = {
    "collapse_navigation": True ,
    "header_links_before_dropdown": 6,
    "navbar_start": ["navbar-logo", "index_link"],
    "navbar_align": "left",
    "show_toc_level": 2,
    "navigation_depth": 2,
    "footer_start": ["copyright"],
    "footer_end": [],
    
    "logo": {
        "image_dark": "_static/img/rivtpy64.png",
        "image_light": "_static/img/rivtpy64.png",
    }
}

favicons = [
    {
        "rel": "icon",
        "sizes": "16x16",
        "href": "favicon-16x16.png",
    },
    {
        "rel": "icon",
        "sizes": "32x32",
        "href": "favicon-32x32.png",
    },

]
