# Automated Post Publishing Script

This script automates the process of creating and publishing blog posts and art posts to Roni Kobrosly's personal website.

## Overview

The script automates the following workflow:
1. Gather post information interactively
2. Create post directory and `contents.lr` file
3. Copy images to post directory
4. Build the Lektor site
5. Deploy to GitHub Pages repository
6. Commit and push changes to both repos

## Prerequisites

- Python 3.12+
- Lektor installed and configured
- Virtual environment activated at `website/bin/activate`
- SSH key configured for GitHub access
- **Note:** The script will automatically clone `ronikobrosly.github.io` if it doesn't exist

## Installation

The script is ready to use - no additional installation required. All dependencies are part of Python's standard library.

## Configuration

Edit `config.py` to customize:
- `DEPLOYED_SITE_REPO` - Path to your deployed GitHub Pages repo
- `DEFAULT_AUTHOR` - Your default author name
- `DEFAULT_TWITTER_HANDLE` - Your default Twitter handle

## Usage

### Basic Usage

```bash
cd posting_script
python publish_post.py
```

Follow the interactive prompts to create your post.

### Dry Run Mode

Preview what the script would do without making any changes:

```bash
python publish_post.py --dry-run
```

This is useful for:
- Testing the script
- Verifying your inputs
- Understanding the workflow

## Interactive Prompts

The script will prompt you for the following information:

### Post Type
- `blog` - Blog post
- `art` - Art post

### Required Fields

**For Blog Posts:**
- Post title
- Author (default: Roni Kobrosly)
- Twitter handle (default: ronikobrosly)
- Publication date (default: today, format: YYYY-MM-DD)
- Summary
- Tags (comma-separated, optional)
- Body text (opens in your default editor)
- Post slug (default: auto-generated from title)
- Path to logo.webp file
- Additional image paths (comma-separated, optional)

**For Art Posts:**
- Post title
- Author (default: Roni Kobrosly)
- Publication date (default: today, format: YYYY-MM-DD)
- Summary (optional)
- Tags (comma-separated, optional)
- Body text (opens in your default editor)
- Post slug (default: auto-generated from title)
- Path to logo.webp file
- Additional image paths (comma-separated, optional)

### Git Configuration
- Path to `ronikobrosly.github.io` repo
- Git commit message for source repo
- Git commit message for deployed site repo (default: same as source)

## Example Session

```
============================================================
Automated Post Publishing Script
============================================================

--- Post Information ---

What type of post? (blog/art): blog
Post title: My Amazing New Blog Post
Author [Roni Kobrosly]:
Twitter handle [ronikobrosly]:
Publication date (YYYY-MM-DD) [2025-10-31]:
Summary: This is a great post about Python and data science.
Tags (comma-separated): python, data science, tutorial

📝 Opening editor for body text...
(Save and close the editor when done)

Post slug (URL-friendly name) [my-amazing-new-blog-post]:
Path to logo.webp file: ~/images/python-logo.webp
Additional image paths (comma-separated, optional):
Path to ronikobrosly.github.io repo [~/Desktop/ronikobrosly.github.io]:
Git commit message for source repo: Add new Python blog post
Git commit message for deployed site repo [Add new Python blog post]:

============================================================
POST PREVIEW
============================================================
Post Type: blog
Title: My Amazing New Blog Post
Author: Roni Kobrosly
Twitter: @ronikobrosly
Date: 2025-10-31
Slug: my-amazing-new-blog-post
Summary: This is a great post about Python and data science.
Tags: python, data science, tutorial
Body: 1250 characters
Logo: /home/ronik/images/python-logo.webp
Additional Images: 0
============================================================

Proceed with publication? (yes/no): yes

✓ Creating post content...
  Created directory: /home/ronik/personal_github_io_website/content/blog/my-amazing-new-blog-post
  Created: /home/ronik/personal_github_io_website/content/blog/my-amazing-new-blog-post/contents.lr
  Copied logo: /home/ronik/personal_github_io_website/content/blog/my-amazing-new-blog-post/logo.webp

✓ Building site...
  Site built successfully!

✓ Deploying to GitHub Pages repo...
  Deployed to: /home/ronik/Desktop/ronikobrosly.github.io
  ✓ Verified google4e956285588bb55a.html is preserved

✓ Committing and pushing changes...
  Committing source repo...
    ✓ Pushed to /home/ronik/personal_github_io_website
  Committing deployed site repo...
    ✓ Pushed to /home/ronik/Desktop/ronikobrosly.github.io
  ✓ All changes pushed successfully!

============================================================
✓ SUCCESS! Your post has been published!
============================================================

Your post is live at:
https://ronikobrosly.github.io/blog/2025/10/31/my-amazing-new-blog-post/
```

## Features

### Safety Features
- **Dry-run mode** - Test without making changes
- **Input validation** - Validates all inputs before proceeding
- **Confirmation prompt** - Preview post before publishing
- **Rollback capability** - Automatically rolls back if an error occurs
- **Google verification file preservation** - Ensures critical file is not lost
- **Auto-clone deployed repo** - Automatically clones the GitHub Pages repo if not found

### Convenience Features
- **Auto-generated slug** - Creates URL-friendly slug from title
- **Default values** - Pre-fills author, Twitter handle, and date
- **External editor** - Opens your preferred editor for body text
- **Relative/absolute paths** - Supports both path formats for images
- **Batch image copying** - Copy multiple images at once

### Error Handling
- Clear error messages for each step
- Validates file existence before copying
- Checks git operations for errors
- Verifies Lektor build succeeds
- Confirms Google verification file is preserved

## Post Structure

The script creates a post directory with the following structure:

```
content/blog/my-post-slug/
├── contents.lr          # Post metadata and content
├── logo.webp           # Featured image
└── additional-img.webp # Optional additional images
```

### contents.lr Format

**Blog Post:**
```
title: Post Title
---
author: Roni Kobrosly
---
twitter_handle: ronikobrosly
---
pub_date: 2025-10-31
---
summary: Post summary goes here...
---
tags:

python
data science
---
body:

Your markdown content here...
```

**Art Post:**
```
title: Art Piece Title
---
author: Roni Kobrosly
---
pub_date: 2025-10-31
---
summary: Optional summary...
---
tags:

digital art
illustration
---
body:

Your markdown content here...
```

## Troubleshooting

### "File not found" error
- Check that the image path is correct
- Use absolute paths (e.g., `/home/ronik/images/logo.webp`)
- Or use paths relative to your home directory (e.g., `~/images/logo.webp`)

### "Git push failed" error
- Ensure your SSH key is configured correctly
- Check that you have push access to both repositories
- Verify you're on the correct branch (main)

### "Lektor build failed" error
- Check the error message for syntax errors in your content
- Ensure the virtual environment is properly activated
- Try running `lektor build` manually to debug

### "Directory not found" error for deployed repo
- The script will automatically clone the repo if it doesn't exist at the specified path
- Ensure your SSH key is configured for GitHub access
- If you want to use an existing clone, provide the correct path when prompted
- Update `DEPLOYED_SITE_REPO` in `config.py` to change the default location

### "google4e956285588bb55a.html was lost" error
- This critical file is needed for Google site verification
- The script will halt if it detects the file is missing
- Ensure the file exists in the deployed repo before running the script

## Editor Configuration

The script uses your system's default editor (from the `EDITOR` environment variable). To change it:

```bash
# In your shell configuration (~/.bashrc or ~/.zshrc)
export EDITOR=vim    # or nano, emacs, code, etc.
```

If `EDITOR` is not set, the script defaults to `nano`.

## Advanced Usage

### Editing Existing Posts

To edit an existing post, manually edit the `contents.lr` file in the post directory, then:

1. Build the site: `lektor build --output-path ./built_website`
2. Copy to deployed repo
3. Commit and push both repos

Or re-run the script with the same slug (will overwrite).

### Custom Deployment Location

Update the deployed repo path in `config.py`:

```python
DEPLOYED_SITE_REPO = Path("/path/to/your/ronikobrosly.github.io")
```

## Support

For issues or questions:
1. Check this README for troubleshooting tips
2. Review the error message carefully
3. Try running with `--dry-run` to debug
4. Check the CLAUDE.md file in the parent directory for additional context

## Future Enhancements

Potential features for future versions:
- Draft mode (create without publishing)
- Edit existing posts
- Preview mode with local server
- Batch operations
- Image optimization
- Tag autocomplete
- Undo last post

---

**Version:** 1.0.0
**Last Updated:** 2025-10-31
