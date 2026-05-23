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

---

## AI Assistant Prompt

If you are working on this project with an AI coding assistant (like ChatGPT, Claude, Gemini, or Copilot), copy and paste the following text into the chat to bootstrap the AI's understanding of this codebase:

```text
You are assisting me in maintaining my academic homepage, which is hosted as a static site on GitHub Pages. 

Here are the key details of the project:
1. **Source & Structure**: This project is a static mirror of klusowski.princeton.edu. The pages are static HTML files located at:
   - Root page: `index.html`
   - Sub-pages: `publications/index.html`, `students/index.html`, `talks/index.html`, and `group/index.html`.
2. **Strict Rule - Relative URLs**: All internal links (e.g. references to pages or assets in `core/`, `profiles/`, `sites/`, `themes/`, `libraries/`) MUST remain relative to support portability across local hosting and different base paths on GitHub Pages (e.g. `../group/` instead of `/group`). Do NOT convert relative links back to absolute root paths (`/`).
3. **Assets**: The static styles, scripts, images, and PDF documents are mirrored in folders (like `sites/`, `profiles/`, `core/`). Maintain this exact folder structure when referencing assets.
4. **Stripped Features**: The Princeton CAS login interfaces and search bars/forms have been intentionally removed from the static pages. Do not try to re-add them.
5. **Fonts**: We use custom Adobe Typekit fonts loaded via `<link rel="stylesheet" href="https://use.typekit.net/oym8vwq.css">`.
6. **Mirroring Utility**: We have a Python script `mirror.py` and test suite `test_mirror.py` to scrape updates from the source site (which bypasses Princeton's bot protection using the header `x-wdsoit-bot-bypass: true`).

Please keep these constraints in mind whenever I ask you to make updates, add publications, modify student details, or tweak pages.
```

