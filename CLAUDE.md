# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Lektor-based static website for Roni Kobrosly's personal portfolio, deployed to GitHub Pages at https://ronikobrosly.github.io/. The site showcases blog posts, art, open-source projects, talks, and professional information.

**Tech Stack:**
- Lektor 3.3.12 (static site generator)
- Python 3.12+
- Jinja2 templating
- terminal.css (retro terminal styling)
- Deployed to GitHub Pages

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
source website/bin/activate

# Install dependencies (if needed)
uv sync
```

### Lektor Commands
```bash
# Start local development server with live reload
lektor server

# Build the site (output to website/)
lektor build

# Clean build artifacts
lektor clean

# Deploy to GitHub Pages (SSH)
lektor deploy gh_ssh

# Deploy to GitHub Pages (HTTPS)
lektor deploy gh_https
```

## Project Architecture

### Directory Structure
```
├── content/              # All content (.lr markdown files)
│   ├── blog/            # Blog posts (blog-post model)
│   ├── art/             # Art gallery (art-post model)
│   ├── open-source/     # Open source projects (project model)
│   ├── talks/           # Conference talks (project model)
│   ├── bio/             # Biography page
│   └── sitemap.xml/     # Auto-generated sitemap
├── models/              # Content type definitions (.ini files)
├── templates/           # Jinja2 templates
│   ├── blocks/         # Flow block templates
│   └── macros/         # Reusable template functions
├── flowblocks/          # Reusable content components (.ini)
├── databags/            # JSON configuration (nav.json for navigation)
├── assets/static/       # Static CSS, JS, images
└── website/             # Build output directory (git-ignored)
```

### Content Models

The site uses 12 Lektor models defined in `models/`:

**Container Models:**
- `blog.ini` - Blog container (pagination: 5 items/page)
- `art.ini` - Art gallery container (pagination: 100 items/page)
- `projects.ini` - Projects carousel
- `testimonials.ini` - Testimonials container

**Content Models:**
- `blog-post.ini` - Individual blog posts with title, author, twitter_handle, pub_date, tags, body
- `art-post.ini` - Individual art pieces with title, author, pub_date, tags, body
- `project.ini` - Projects/talks with flow blocks (flexible content composition)
- `page.ini` - Simple pages with title and body
- `testimonial.ini` - Individual testimonials
- `resume.ini` - Resume page with flow blocks (experience, education, skills)
- `all-tags.ini` - Tag index page
- `html.ini` - Raw HTML pages

### Flow Blocks

Flow blocks enable flexible content composition. Available types:

**Project Flow Blocks:**
- `youtube` - Embed YouTube videos
- `description` - Text descriptions (markdown)
- `github` - GitHub repository links
- `resource` - External resource links
- `slides` - Presentation slides
- `notebooks` - Jupyter notebook links
- `book` - Book references

**Resume Flow Blocks:**
- `resume-experience` - Work experience entries
- `resume-education` - Education entries
- `resume-skills` - Skills listing

### Slug Format

Blog and art posts use date-based slugs:
- Format: `y/M/d/{id}`
- Example: `/blog/24/10/15/my-post-title/`

### Plugins

Configured in `personal-site.lektorproject`:
- `lektor-markdown-header-anchors` (0.3) - Auto-generates anchor links
- `lektor-markdown-highlighter` (0.3.2) - Syntax highlighting with Pygments
- `lektor-atom` (0.4.0) - Atom/RSS feed generation at `/feed.xml`
- `lektor-tags` (0.5.2) - Tag support; auto-generates `/blog/tag/{tag-name}/` pages

### Template Macros

Reusable rendering functions in `templates/macros/`:

**Blog Macros (`blog.html`):**
- `render_blog_post()` - Full blog post with metadata
- `render_blog_card()` - Compact card for listings
- `render_author_tags()` - Author + tag links
- `render_reading_time()` - Calculates reading time (200 words/minute)
- `render_meta_tags()` - OpenGraph metadata for SEO

**Other Macros:**
- `render_art_post()`, `render_art_card()` - Art gallery rendering
- `render_project()` - Project display with flow blocks
- `render_pagination()` - Previous/next controls
- `render_slideshow()` - Image carousel

### Navigation

Navigation is driven by `/databags/nav.json` with header and footer arrays. The base template (`layout.html`) reads this to dynamically generate navigation links.

### Styling

- Uses **terminal.css** (v0.7.2) for retro terminal aesthetic
- Custom styles in `layout.html` for card layouts
- Active navigation shown with terminal-style cursor
- Responsive flex containers for blog/art cards

### Analytics

Google Analytics is integrated in `layout.html` with tracking ID: `G-TT9MYHW754`

## Common Tasks

### Creating a New Blog Post

1. Create directory: `content/blog/{slug}/`
2. Create `contents.lr` with fields:
   ```
   title: Post Title
   ---
   author: Roni Kobrosly
   ---
   twitter_handle: ronikobrosly
   ---
   pub_date: 2024-10-30
   ---
   tags: tag1, tag2
   ---
   body:

   Your markdown content here...
   ```
3. Optional: Add `logo.webp` for featured image
4. Tags automatically generate index pages at `/blog/tag/{tag-name}/`

### Creating a New Art Piece

1. Create directory: `content/art/{piece-name}/`
2. Create `contents.lr` with `art-post` model fields
3. Add image attachments as needed

### Adding a New Project

1. Create directory: `content/open-source/{project-name}/` or `content/talks/{talk-name}/`
2. Use flow blocks for flexible content composition
3. Available blocks: description, youtube, github, resource, slides, notebooks, book

### Modifying Navigation

Edit `/databags/nav.json`:
- `header` array - Top navigation links
- `footer` array - Bottom social/contact links

### Deployment Targets

Configured in `personal-site.lektorproject`:
- `gh_ssh` - Deploy via SSH: `lektor deploy gh_ssh`
- `gh_https` - Deploy via HTTPS: `lektor deploy gh_https`

Target repository: `ronikobrosly/ronikobrosly.github.io`

## Key File Locations

- Main config: `/home/ronik/personal_github_io_website/personal-site.lektorproject`
- Python config: `/home/ronik/personal_github_io_website/pyproject.toml`
- Base template: `/home/ronik/personal_github_io_website/templates/layout.html`
- Navigation data: `/home/ronik/personal_github_io_website/databags/nav.json`
- Models directory: `/home/ronik/personal_github_io_website/models/`
- Content root: `/home/ronik/personal_github_io_website/content/`

## Notes

- Build output goes to `website/` directory (git-ignored)
- Blog pagination: 5 posts per page
- Art pagination: 100 pieces per page
- Content ordering: By `-pub_date` (newest first), then title
- Virtual environment located at `website/bin/activate`
- No test suite configured for this project
- Feed automatically generated at `/feed.xml` and `/blog/feed.xml`




## For Claude: Plan for migrating from terminal.css to panr/terminal-css 

### Overview

This guide will help you switch from Terminal CSS (terminalcss.xyz) to panr/terminal-css (https://github.com/panr/terminal-css) while maintaining all your Lektor functionality.

Note: I do not want to change any of the functional elements of my website like the tagging system, pagination, dates, summaries sections, body text, images, etc. All of this should work as it currently does after the migration. I just want to change the CSS. 


### Switching from Terminal CSS to panr/terminal-css in Your Lektor Website

#### Key Differences Between the Two Frameworks

**Terminal CSS (terminalcss.xyz):**
- Requires specific CSS classes on elements
- Uses `<body class="terminal">` for consistent styling
- Version 0.7.5

**panr/terminal-css:**
- **Classless** - styles semantic HTML directly without classes
- Derived from the Hugo Terminal theme
- Simpler implementation
- Modern, retro terminal aesthetic

#### Step-by-Step Migration Process

In the root project directory, you'll find the following three files. Please incorporate them into the updated website. 

* `terminal.css`: The new terminal.css file I want to use, created at `https://panr.github.io/hugo-theme-terminal-demo/`
* `favicon.png`: The new favicon image
* `og-image.png`: The Open Graph image


##### Step 1: Remove Old Terminal CSS

1. **Locate your current CSS link** in your Lektor templates (likely in `templates/layout.html` or similar):
   ```html
   <!-- OLD - Remove this -->
   <link rel="stylesheet" href="https://unpkg.com/terminal.css@0.7.5/dist/terminal.min.css" />
   ```

2. **Remove any Terminal CSS classes** from your HTML templates:
   - Remove `class="terminal"` from `<body>` tags
   - Remove any other Terminal CSS-specific classes

##### Step 2: Add panr/terminal-css

Add the new CSS link to your main layout template (typically `templates/layout.html`):

```html
<!-- Add this in your <head> section -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@panr/terminal-css@1.0.1/terminal.min.css">
```

Then reference it locally:
```html
<link rel="stylesheet" href="{{ '/static/css/terminal.min.css'|url }}">
```

##### Step 3: Customize the Color Scheme (Optional)

The new `terminal.css` should have the updated color scheme included!

##### Step 4: Update Your Templates

The great news is that panr/terminal-css is classless, so if you're using semantic HTML, it should work automatically. Here's how to ensure compatibility:

###### For Blog Posts
```html
<!-- templates/blog-post.html -->
<article>
  <header>
    <h1>{{ this.title }}</h1>
    <time datetime="{{ this.pub_date|dateformat('Y-m-d') }}">
      {{ this.pub_date|dateformat('F d, Y') }}
    </time>
  </header>
  
  {{ this.body }}
  
  {% if this.tags %}
  <footer>
    <p>Tags:
    {% for tag in this.tags %}
      <a href="{{ ('/blog/tag/' ~ tag)|url }}">#{{ tag }}</a>
    {% endfor %}
    </p>
  </footer>
  {% endif %}
</article>
```

###### For Blog Listing Pages
```html
<!-- templates/blog.html -->
<main>
  <h1>{{ this.title }}</h1>
  
  {% for post in this.children %}
  <article>
    <h2><a href="{{ post|url }}">{{ post.title }}</a></h2>
    <time datetime="{{ post.pub_date|dateformat('Y-m-d') }}">
      {{ post.pub_date|dateformat('F d, Y') }}
    </time>
    {% if post.summary %}
    <p>{{ post.summary }}</p>
    {% endif %}
    <a href="{{ post|url }}">Read more →</a>
  </article>
  {% endfor %}
</main>
```

###### For Images
```html
<!-- Images work automatically with semantic HTML -->
<figure>
  <img src="{{ '/images/photo.jpg'|url }}" alt="Description">
  <figcaption>Your image caption</figcaption>
</figure>
```

##### Step 5: Test Your Site

1. **Build your Lektor site**:
   ```bash
   lektor build
   ```

2. **Run local server**:
   ```bash
   lektor server
   ```

3. **Check these elements**:
   - [ ] Blog post titles (h1, h2, etc.)
   - [ ] Dates display correctly
   - [ ] Tags/categories render properly
   - [ ] Body text and paragraphs
   - [ ] Images with captions
   - [ ] Links and navigation
   - [ ] Code blocks (if you have any)
   - [ ] Blockquotes
   - [ ] Lists (ordered and unordered)

##### Step 6: Fine-Tune with Custom CSS (If Needed)

If you need to adjust specific elements, create a `custom.css` file:

```css
/* assets/static/css/custom.css */

/* Adjust spacing between blog posts */
article + article {
  margin-top: 3rem;
}

/* Style post metadata */
article time {
  display: block;
  margin: 0.5rem 0;
  opacity: 0.8;
}

/* Style tags */
article footer a {
  margin-right: 0.5rem;
}

/* Add separator between posts on listing page */
article:not(:last-child) {
  padding-bottom: 2rem;
  border-bottom: 1px dashed var(--border, #ccc);
}
```

#### Troubleshooting

##### Issue: Elements Don't Look Styled
**Solution**: Ensure you're using proper semantic HTML. panr/terminal-css styles these elements:
- `<h1>` through `<h6>` for headings
- `<p>` for paragraphs
- `<a>` for links
- `<article>` for blog posts
- `<time>` for dates
- `<figure>` and `<figcaption>` for images
- `<blockquote>` for quotes
- `<ul>`, `<ol>`, `<li>` for lists
- `<pre>`, `<code>` for code blocks


#### Additional Resources

- **panr/terminal-css GitHub**: https://github.com/panr/terminal-css
- **Terminal.css Generator**: https://panr.github.io/terminal-css/
- **Lektor Documentation**: https://www.getlektor.com/docs/
- **Hugo Terminal Theme Demo** (for design inspiration): https://panr.github.io/hugo-theme-terminal-demo/
