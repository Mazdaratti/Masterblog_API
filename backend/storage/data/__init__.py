"""
Initialization for the data module, including the path to the blog data file.

This module defines the path to the `blog.json` file, which stores the blog posts.
It uses the `Path` module for working with paths in a platform-independent way, and
the `os` module to get the current directory and set the full file path for `blog.json`.

Attributes:
    CUR_DIR (Path): The current directory where this file is located.
    PATH (str): The full file path to the `blog.json` file,
    located in the same directory as this module.
"""
from pathlib import Path
import os

CUR_DIR = Path(__file__).parent
PATH = os.path.join(CUR_DIR, 'blog.json')
