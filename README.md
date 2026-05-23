# klusowski.princeton.edu Static Mirror

This repository contains the static mirror of [klusowski.princeton.edu](https://klusowski.princeton.edu), hosted on GitHub Pages at [pu-orfe.github.io/klusowski](https://pu-orfe.github.io/klusowski/).

## Project Structure

* `/` - The root directory contains the static files served by GitHub Pages.
* `publications/`, `students/`, `talks/`, `group/` - Sub-pages mapped to clean relative directories.
* `core/`, `profiles/`, `sites/`, `themes/`, `libraries/` - Static assets, images, CSS stylesheets, JavaScript files, and documents downloaded from the original site.
* `.nojekyll` - Bypasses GitHub Pages' default Jekyll build processor so that assets starting with underscores or dots are served correctly.
* `mirror.py` - The crawler script to scrape the site, download new files, and rewrite URLs.
* `test_mirror.py` - Unit test suite for URL rewriting logic.
* `Dockerfile` & `docker-compose.yml` - Docker setup to run the test suite in a containerized environment.

## Mirror & Crawl Details

The static pages were downloaded by bypassing the bot protection block (using the `x-wdsoit-bot-bypass` header) and rewritten to convert all absolute links (like `/sites/...`) to clean relative references (like `../sites/...`). 

The login interface and the search forms/toggles have been stripped out. The fonts are loaded from a license-covered custom Typekit stylesheet.

---

## Local Development & Testing

### Running Tests
To run unit tests for the URL rewriter inside the Docker container:
```bash
docker-compose up --build
```

### Running the Mirror Script
To refresh the static mirror (requires the bypass header configured inside the script):
1. Set up a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the crawler:
   ```bash
   python3 mirror.py
   ```
