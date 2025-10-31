#!/usr/bin/env python3
"""
Automated Post Publishing Script for Roni Kobrosly's Personal Website

This script automates the process of creating and publishing blog posts and art posts
to the Lektor-based static website.

Usage:
    python publish_post.py [--dry-run] [--just-rebuild]

Options:
    --dry-run        Preview what would happen without making any changes
    --just-rebuild   Rebuild and deploy the site without creating a new post
                     (useful for CSS/template changes)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Import configuration
import config


class PostPublisher:
    """Main class for handling post creation and publication."""

    def __init__(self, dry_run=False, just_rebuild=False):
        self.dry_run = dry_run
        self.just_rebuild = just_rebuild
        self.post_data = {}
        self.post_type = None
        self.post_slug = None
        self.post_dir = None

    def run(self):
        """Main execution flow."""
        print("=" * 60)
        print("Automated Post Publishing Script")
        print("=" * 60)

        if self.dry_run:
            print("\n[DRY RUN MODE - No changes will be made]\n")

        if self.just_rebuild:
            print("\n[JUST REBUILD MODE - No new post will be created]\n")
            return self.run_just_rebuild()

        try:
            # Step 1: Gather post information
            self.gather_post_info()

            # Step 2: Preview and confirm
            if not self.confirm_post():
                print("\n❌ Publication cancelled.")
                return False

            # Step 3: Create post content
            self.create_post_content()

            # Step 4: Build site
            self.build_site()

            # Step 5: Deploy to GitHub Pages repo
            self.deploy_site()

            # Step 6: Git operations
            self.commit_and_push()

            # Success!
            print("\n" + "=" * 60)
            print("✓ SUCCESS! Your post has been published!")
            print("=" * 60)

            # Generate and display the post URL
            pub_date = datetime.strptime(self.post_data['pub_date'], '%Y-%m-%d')
            url = f"https://ronikobrosly.github.io/{self.post_type}/{pub_date.year}/{pub_date.month}/{pub_date.day}/{self.post_slug}/"
            print(f"\nYour post is live at:\n{url}")

            return True

        except KeyboardInterrupt:
            print("\n\n❌ Operation cancelled by user.")
            return False
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            print("\nRolling back changes...")
            self.rollback()
            return False

    def run_just_rebuild(self):
        """Rebuild and deploy the site without creating a new post."""
        try:
            print("\n--- Rebuild Configuration ---\n")

            # Get deployed repo path (and clone if needed)
            default_repo = str(config.DEPLOYED_SITE_REPO)
            repo_path = self.get_input(
                "Path to ronikobrosly.github.io repo",
                default=default_repo
            )
            repo_path = Path(repo_path).expanduser()

            # Clone repo if it doesn't exist
            if not repo_path.exists():
                print(f"\n📦 Repository not found at {repo_path}")
                print("Cloning ronikobrosly/ronikobrosly.github.io...")
                self.clone_deployed_repo(repo_path)

            self.post_data['deployed_repo'] = repo_path

            # Get git commit messages
            self.post_data['commit_msg_source'] = self.get_input(
                "Git commit message for source repo",
                required=True
            )

            default_commit_deployed = self.post_data['commit_msg_source']
            self.post_data['commit_msg_deployed'] = self.get_input(
                "Git commit message for deployed site repo",
                default=default_commit_deployed
            )

            # Confirm before proceeding
            print("\n" + "=" * 60)
            print("REBUILD PREVIEW")
            print("=" * 60)
            print(f"Deployed repo: {self.post_data['deployed_repo']}")
            print(f"Source commit: {self.post_data['commit_msg_source']}")
            print(f"Deployed commit: {self.post_data['commit_msg_deployed']}")
            print("=" * 60)

            if not self.dry_run:
                response = input("\nProceed with rebuild and deployment? (yes/no): ").strip().lower()
                if response not in ['yes', 'y']:
                    print("\n❌ Rebuild cancelled.")
                    return False

            # Build site
            self.build_site()

            # Deploy to GitHub Pages repo
            self.deploy_site()

            # Git operations
            self.commit_and_push()

            # Success!
            print("\n" + "=" * 60)
            print("✓ SUCCESS! Website rebuilt and deployed!")
            print("=" * 60)
            print("\nYour changes are live at:\nhttps://ronikobrosly.github.io/")

            return True

        except KeyboardInterrupt:
            print("\n\n❌ Operation cancelled by user.")
            return False
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            return False

    def gather_post_info(self):
        """Gather all information needed for the post."""
        print("\n--- Post Information ---\n")

        # Post type
        while True:
            post_type = input("What type of post? (blog/art): ").strip().lower()
            if post_type in ['blog', 'art']:
                self.post_type = post_type
                break
            print("Invalid post type. Please enter 'blog' or 'art'.")

        # Title
        self.post_data['title'] = self.get_input("Post title", required=True)

        # Generate default slug from title
        default_slug = self.generate_slug(self.post_data['title'])

        # Author
        self.post_data['author'] = self.get_input(
            "Author",
            default=config.DEFAULT_AUTHOR
        )

        # Twitter handle (blog posts only)
        if self.post_type == 'blog':
            self.post_data['twitter_handle'] = self.get_input(
                "Twitter handle",
                default=config.DEFAULT_TWITTER_HANDLE
            )

        # Publication date
        default_date = datetime.now().strftime('%Y-%m-%d')
        while True:
            pub_date = self.get_input("Publication date (YYYY-MM-DD)", default=default_date)
            if self.validate_date(pub_date):
                self.post_data['pub_date'] = pub_date
                break
            print("Invalid date format. Please use YYYY-MM-DD.")

        # Summary
        self.post_data['summary'] = self.get_input("Summary", required=True)

        # Tags
        tags_input = self.get_input("Tags (comma-separated)", required=False)
        if tags_input:
            self.post_data['tags'] = '\n'.join([tag.strip() for tag in tags_input.split(',')])
        else:
            self.post_data['tags'] = ''

        # Body text (use editor)
        print("\n📝 Opening editor for body text...")
        print("(Save and close the editor when done)")
        self.post_data['body'] = self.get_text_from_editor()

        # Post slug
        self.post_slug = self.get_input("Post slug (URL-friendly name)", default=default_slug)

        # Logo image
        while True:
            logo_path = self.get_input("Path to logo.webp file", required=True)
            logo_path = Path(logo_path).expanduser()
            if logo_path.exists():
                self.post_data['logo_path'] = logo_path
                break
            print(f"File not found: {logo_path}")

        # Additional images
        additional_images_input = self.get_input(
            "Additional image paths (comma-separated)",
            required=False
        )
        if additional_images_input:
            self.post_data['additional_images'] = [
                Path(p.strip()).expanduser()
                for p in additional_images_input.split(',')
            ]
        else:
            self.post_data['additional_images'] = []

        # Deployed site repo path - clone if needed
        default_repo = str(config.DEPLOYED_SITE_REPO)
        repo_path = self.get_input(
            "Path to ronikobrosly.github.io repo",
            default=default_repo
        )
        repo_path = Path(repo_path).expanduser()

        # Clone repo if it doesn't exist
        if not repo_path.exists():
            print(f"\n📦 Repository not found at {repo_path}")
            print("Cloning ronikobrosly/ronikobrosly.github.io...")
            self.clone_deployed_repo(repo_path)

        self.post_data['deployed_repo'] = repo_path

        # Git commit messages
        self.post_data['commit_msg_source'] = self.get_input(
            "Git commit message for source repo",
            required=True
        )

        default_commit_deployed = self.post_data['commit_msg_source']
        self.post_data['commit_msg_deployed'] = self.get_input(
            "Git commit message for deployed site repo",
            default=default_commit_deployed
        )

    def confirm_post(self):
        """Display post preview and ask for confirmation."""
        print("\n" + "=" * 60)
        print("POST PREVIEW")
        print("=" * 60)
        print(f"Post Type: {self.post_type}")
        print(f"Title: {self.post_data['title']}")
        print(f"Author: {self.post_data['author']}")
        if 'twitter_handle' in self.post_data:
            print(f"Twitter: @{self.post_data['twitter_handle']}")
        print(f"Date: {self.post_data['pub_date']}")
        print(f"Slug: {self.post_slug}")
        print(f"Summary: {self.post_data['summary'][:100]}...")
        print(f"Tags: {self.post_data['tags'].replace(chr(10), ', ') if self.post_data['tags'] else 'None'}")
        print(f"Body: {len(self.post_data['body'])} characters")
        print(f"Logo: {self.post_data['logo_path']}")
        print(f"Additional Images: {len(self.post_data['additional_images'])}")
        print("=" * 60)

        if self.dry_run:
            return True

        response = input("\nProceed with publication? (yes/no): ").strip().lower()
        return response in ['yes', 'y']

    def create_post_content(self):
        """Create the post directory and contents.lr file."""
        print("\n✓ Creating post content...")

        # Determine post directory
        content_dir = config.POST_TYPES[self.post_type]['content_dir']
        self.post_dir = content_dir / self.post_slug

        if self.dry_run:
            print(f"  [DRY RUN] Would create directory: {self.post_dir}")
            return

        # Create directory
        self.post_dir.mkdir(parents=True, exist_ok=False)
        print(f"  Created directory: {self.post_dir}")

        # Load template
        template_file = config.PROJECT_ROOT / "posting_script" / "templates" / f"{self.post_type}_post.lr"
        with open(template_file, 'r') as f:
            template = f.read()

        # Fill in template
        content = template.format(
            title=self.post_data['title'],
            author=self.post_data['author'],
            twitter_handle=self.post_data.get('twitter_handle', ''),
            pub_date=self.post_data['pub_date'],
            summary=self.post_data['summary'],
            tags=self.post_data['tags'],
            body=self.post_data['body']
        )

        # Write contents.lr
        contents_file = self.post_dir / "contents.lr"
        with open(contents_file, 'w') as f:
            f.write(content)
        print(f"  Created: {contents_file}")

        # Copy logo
        logo_dest = self.post_dir / "logo.webp"
        shutil.copy2(self.post_data['logo_path'], logo_dest)
        print(f"  Copied logo: {logo_dest}")

        # Copy additional images
        for img_path in self.post_data['additional_images']:
            if img_path.exists():
                img_dest = self.post_dir / img_path.name
                shutil.copy2(img_path, img_dest)
                print(f"  Copied image: {img_dest}")

    def build_site(self):
        """Build the Lektor site."""
        print("\n✓ Building site...")

        if self.dry_run:
            print("  [DRY RUN] Would run: lektor build --output-path ./built_website")
            return

        # Build command
        cmd = f"source {config.VENV_ACTIVATE} && lektor build --output-path {config.BUILD_OUTPUT}"

        result = subprocess.run(
            cmd,
            shell=True,
            cwd=config.PROJECT_ROOT,
            capture_output=True,
            text=True,
            executable='/bin/bash'
        )

        if result.returncode != 0:
            raise Exception(f"Lektor build failed:\n{result.stderr}")

        print("  Site built successfully!")

    def deploy_site(self):
        """Deploy the built site to the GitHub Pages repo."""
        print("\n✓ Deploying to GitHub Pages repo...")

        deployed_repo = self.post_data['deployed_repo']

        if self.dry_run:
            print(f"  [DRY RUN] Would copy {config.BUILD_OUTPUT}/* to {deployed_repo}/")
            print(f"  [DRY RUN] Would preserve {config.GOOGLE_VERIFICATION_FILE}")
            return

        # Verify Google verification file exists in deployed repo
        verification_file = deployed_repo / config.GOOGLE_VERIFICATION_FILE
        if not verification_file.exists():
            print(f"  ⚠️  Warning: {config.GOOGLE_VERIFICATION_FILE} not found in deployed repo!")

        # Copy all files from built_website to deployed repo
        for item in config.BUILD_OUTPUT.iterdir():
            dest = deployed_repo / item.name
            if item.is_file():
                shutil.copy2(item, dest)
            elif item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)

        print(f"  Deployed to: {deployed_repo}")

        # Verify Google verification file is still there
        if verification_file.exists():
            print(f"  ✓ Verified {config.GOOGLE_VERIFICATION_FILE} is preserved")
        else:
            raise Exception(f"{config.GOOGLE_VERIFICATION_FILE} was lost during deployment!")

    def commit_and_push(self):
        """Commit and push changes to both repos."""
        print("\n✓ Committing and pushing changes...")

        # Commit source repo
        print(f"  Committing source repo...")
        self.git_commit_push(
            config.PROJECT_ROOT,
            self.post_data['commit_msg_source']
        )

        # Commit deployed repo
        print(f"  Committing deployed site repo...")
        self.git_commit_push(
            self.post_data['deployed_repo'],
            self.post_data['commit_msg_deployed']
        )

        print("  ✓ All changes pushed successfully!")

    def clone_deployed_repo(self, repo_path):
        """Clone the deployed GitHub Pages repository."""
        if self.dry_run:
            print(f"  [DRY RUN] Would clone ronikobrosly/ronikobrosly.github.io to {repo_path}")
            return

        # Create parent directory if needed
        repo_path.parent.mkdir(parents=True, exist_ok=True)

        # Clone the repository
        repo_url = "git@github.com:ronikobrosly/ronikobrosly.github.io.git"

        result = subprocess.run(
            ['git', 'clone', repo_url, str(repo_path)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"Git clone failed:\n{result.stderr}")

        print(f"  ✓ Repository cloned to {repo_path}")

        # Verify Google verification file exists
        verification_file = repo_path / config.GOOGLE_VERIFICATION_FILE
        if not verification_file.exists():
            print(f"  ⚠️  Warning: {config.GOOGLE_VERIFICATION_FILE} not found in cloned repo!")

    def git_commit_push(self, repo_path, commit_message):
        """Execute git add, commit, and push in the specified repo."""
        if self.dry_run:
            print(f"    [DRY RUN] Would commit to {repo_path}")
            print(f"    [DRY RUN] Commit message: {commit_message}")
            return

        # Git add
        result = subprocess.run(
            ['git', 'add', '.'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Git add failed:\n{result.stderr}")

        # Git commit
        result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # Check if there's nothing to commit
            if "nothing to commit" in result.stdout:
                print(f"    No changes to commit in {repo_path}")
                return
            raise Exception(f"Git commit failed:\n{result.stderr}")

        # Git push
        result = subprocess.run(
            ['git', 'push'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Git push failed:\n{result.stderr}")

        print(f"    ✓ Pushed to {repo_path}")

    def rollback(self):
        """Rollback changes if something goes wrong."""
        if self.dry_run:
            return

        if self.post_dir and self.post_dir.exists():
            print(f"Removing post directory: {self.post_dir}")
            shutil.rmtree(self.post_dir)

        print("Rollback complete.")

    # Utility methods

    def get_input(self, prompt, default=None, required=False):
        """Get input from user with optional default value."""
        if default:
            prompt_text = f"{prompt} [{default}]: "
        else:
            prompt_text = f"{prompt}: "

        while True:
            value = input(prompt_text).strip()

            if not value and default:
                return default

            if not value and required:
                print("This field is required.")
                continue

            return value

    def get_text_from_editor(self):
        """Open user's default editor for multi-line text input."""
        editor = os.environ.get('EDITOR', 'nano')

        with tempfile.NamedTemporaryFile(mode='w+', suffix='.md', delete=False) as tf:
            temp_file = tf.name

        try:
            subprocess.run([editor, temp_file], check=True)

            with open(temp_file, 'r') as f:
                content = f.read().strip()

            return content
        finally:
            if Path(temp_file).exists():
                Path(temp_file).unlink()

    def generate_slug(self, title):
        """Generate a URL-friendly slug from a title."""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        return slug

    def validate_date(self, date_str):
        """Validate date string is in YYYY-MM-DD format."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Automated Post Publishing Script'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would happen without making changes'
    )
    parser.add_argument(
        '--just-rebuild',
        action='store_true',
        help='Rebuild and deploy the site without creating a new post (for CSS/template changes)'
    )

    args = parser.parse_args()

    publisher = PostPublisher(dry_run=args.dry_run, just_rebuild=args.just_rebuild)
    success = publisher.run()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
