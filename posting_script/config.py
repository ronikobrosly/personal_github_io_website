"""
Configuration file for the automated post publishing script.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
BUILD_OUTPUT = PROJECT_ROOT / "built_website"
VENV_ACTIVATE = PROJECT_ROOT / "website" / "bin" / "activate"

# Deployed site repo (user should configure this)
# Default location - can be overridden via prompt
DEPLOYED_SITE_REPO = Path.home() / "Desktop" / "ronikobrosly.github.io"

# Google verification file (critical - must be preserved)
GOOGLE_VERIFICATION_FILE = "google4e956285588bb55a.html"

# Defaults
DEFAULT_AUTHOR = "Roni Kobrosly"
DEFAULT_TWITTER_HANDLE = "ronikobrosly"

# Post types configuration
POST_TYPES = {
    "blog": {
        "content_dir": CONTENT_DIR / "blog",
        "model": "blog-post",
        "required_fields": ["title", "author", "twitter_handle", "pub_date", "summary", "body"],
        "optional_fields": ["tags"]
    },
    "art": {
        "content_dir": CONTENT_DIR / "art",
        "model": "art-post",
        "required_fields": ["title", "author", "pub_date", "body"],
        "optional_fields": ["tags", "summary"]
    }
}

# Supported image formats
SUPPORTED_IMAGE_FORMATS = [".webp", ".jpg", ".jpeg", ".png", ".gif"]

# Git configuration
GIT_BRANCH = "main"
