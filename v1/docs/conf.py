# -*- coding: utf-8 -*-
import os
import re
import sys

sys.path.append(os.path.abspath("./demo/"))

project = "opulence"
version = "0.42"
author = "Louis Jurczyk"
language = "en"

extensions = ["sphinx.ext.autosectionlabel", "sphinx.ext.autodoc", "sphinx_rtd_theme"]

source_suffix = ".rst"
master_doc = "index"

html_theme = "sphinx_rtd_theme"
html_logo = "demo/static/logo-wordmark-light.svg"
