from datetime import datetime

import hyperspy_gui_anywidget

project = "hyperspy_gui_anywidget"
copyright = f"{datetime.today().year}, The HyperSpy developers"
author = "The HyperSpy developers"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

exclude_patterns = ["_build"]
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}
master_doc = "index"

release = hyperspy_gui_anywidget.__version__
version = ".".join(release.split(".")[:2])

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/hyperspy/hyperspy_gui_anywidget",
}
html_static_path = []
