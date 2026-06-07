import os
import urllib.parse
import requests
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://klusowski.princeton.edu"
BYPASS_HEADER = {"x-wdsoit-bot-bypass": "true", "User-Agent": "Mozilla/5.0"}
TYPEKIT_URL = "https://use.typekit.net/oym8vwq.css"

LOCAL_PAGES = {
    '/': 'index.html',
    '/publications': 'publications/index.html',
    '/students': 'students/index.html',
    '/talks': 'talks/index.html',
    '/group': 'group/index.html'
}

def get_depth(page_path):
    """Calculates the depth of a page path relative to root."""
    if page_path == '/':
        return 0
    stripped = page_path.strip('/')
    if not stripped:
        return 0
    return stripped.count('/') + 1

def get_relative_prefix(depth):
    """Generates relative path prefix (e.g. '../') based on depth."""
    return "../" * depth

def clean_path(url_path):
    """Strips query parameters and fragment identifiers."""
    parsed = urllib.parse.urlparse(url_path)
    return parsed.path

def rewrite_url(current_page_path, url):
    """
    Rewrites absolute/relative URLs in HTML to correct relative paths.
    Returns:
      - None if it's an external link or special protocol.
      - '__TYPEKIT__' if it is an Adobe Typekit CSS file.
      - The rewritten relative URL string for local pages/assets.
    """
    if not url:
        return url
    
    # Check for special protocols or anchors
    url_lower = url.lower()
    if url_lower.startswith(('mailto:', 'tel:', 'javascript:', '#')):
        return url
        
    parsed = urllib.parse.urlparse(url)
    
    # Adobe Typekit check
    if parsed.hostname == 'use.typekit.net':
        return "__TYPEKIT__"
        
    # Check domain
    if parsed.netloc and parsed.netloc != "klusowski.princeton.edu":
        return url
        
    # Extract path and normalize
    path = parsed.path if parsed.path else '/'
    fragment = parsed.fragment
    
    # Normalize: strip trailing slash unless it's root
    norm_path = path
    if norm_path.endswith('/') and len(norm_path) > 1:
        norm_path = norm_path[:-1]

    # Map homepage back to root page
    if norm_path == '/homepage':
        norm_path = '/'

    # Map caslogin to Princeton external domain CAS login
    if norm_path == '/caslogin':
        return "https://klusowski.princeton.edu/caslogin"
        
    depth = get_depth(current_page_path)
    prefix = get_relative_prefix(depth)
    
    # Scenario 1: It is one of the local mirrored pages
    if norm_path in LOCAL_PAGES:
        if norm_path == '/':
            rel_link = prefix if prefix else './'
        else:
            rel_link = prefix + norm_path.lstrip('/') + '/'
            
        if fragment:
            rel_link += f"#{fragment}"
        return rel_link
        
    # Scenario 2: It is a local asset file (CSS, JS, Image, PDF etc.)
    clean_asset_path = norm_path.lstrip('/')
    rel_link = prefix + clean_asset_path
    if fragment:
        rel_link += f"#{fragment}"
    return rel_link

def download_file(url, output_path):
    """Downloads a file from url and saves it to output_path."""
    # Prevent downloading external/absolute URLs without domain
    if not url.startswith("http"):
        url = urllib.parse.urljoin(BASE_URL, url)
        
    print(f"Downloading: {url} -> {output_path}")
    
    try:
        response = requests.get(url, headers=BYPASS_HEADER, stream=True)
        response.raise_for_status()
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"FAILED to download {url}: {e}")

def rewrite_html(html_content, current_page_path, discovered_assets):
    """
    Parses HTML content, replaces all local asset/page URLs,
    configures Typekit stylesheet, and tracks discovered assets.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove existing typekit links
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href and rewrite_url(current_page_path, href) == "__TYPEKIT__":
            link.decompose()
            
    # Add our typekit stylesheet in the head
    head = soup.find('head')
    if head:
        new_tk = soup.new_tag('link', rel='stylesheet', href=TYPEKIT_URL)
        head.append(new_tk)

    # Remove search bar interface
    search_bar = soup.find(id='search-bar') or soup.find(class_='search-bar')
    if search_bar:
        search_bar.decompose()
        
    # Remove skip to search link
    skip_search = soup.find('a', href='#edit-search-keys')
    if skip_search:
        skip_search.decompose()
        
    # Remove utility menu (typically containing login link)
    utility_menu = soup.find(class_='utility-menu')
    if utility_menu:
        utility_menu.decompose()
        
    # Remove any other login link or its parent LI
    for login_link in soup.find_all('a', class_=lambda c: c and ('ps-login-link' in c or 'ps-login-logout-link' in c)):
        li = login_link.find_parent('li')
        if li:
            li.decompose()
        else:
            login_link.decompose()
        
    # Helper to rewrite tag attributes
    def process_attr(tag, attr):
        val = tag.get(attr)
        if not val:
            return
            
        rewritten = rewrite_url(current_page_path, val)
        if rewritten == "__TYPEKIT__":
            # Handled separately
            return
            
        if rewritten != val:
            tag[attr] = rewritten
            
        # If it's a local asset, track it for download
        # (Exclude external links, anchor-only, special protocols, and mapped pages)
        parsed = urllib.parse.urlparse(val)
        if (not parsed.netloc or parsed.netloc == "klusowski.princeton.edu") and not val.lower().startswith(('mailto:', 'tel:', 'javascript:', '#')):
            norm_path = parsed.path if parsed.path else '/'
            if norm_path.endswith('/') and len(norm_path) > 1:
                norm_path = norm_path[:-1]
            if norm_path not in LOCAL_PAGES:
                discovered_assets.add(norm_path)

    # Process tags
    for tag in soup.find_all(['link', 'script', 'img', 'a', 'source', 'embed', 'object']):
        if tag.name == 'link':
            process_attr(tag, 'href')
        elif tag.name == 'script':
            process_attr(tag, 'src')
        elif tag.name == 'img':
            process_attr(tag, 'src')
            # Handle srcset if present
            srcset = tag.get('srcset')
            if srcset:
                parts = []
                for entry in srcset.split(','):
                    entry = entry.strip()
                    if not entry:
                        continue
                    subparts = entry.split()
                    if not subparts:
                        continue
                    img_url = subparts[0]
                    rewritten_img = rewrite_url(current_page_path, img_url)
                    if rewritten_img != img_url:
                        subparts[0] = rewritten_img
                    parts.append(" ".join(subparts))
                    # Add to assets
                    parsed = urllib.parse.urlparse(img_url)
                    if not parsed.netloc or parsed.netloc == "klusowski.princeton.edu":
                        norm_path = parsed.path if parsed.path else '/'
                        if norm_path not in LOCAL_PAGES:
                            discovered_assets.add(norm_path)
                tag['srcset'] = ", ".join(parts)
        elif tag.name == 'a':
            process_attr(tag, 'href')
        elif tag.name == 'source':
            process_attr(tag, 'src')
            # Handle srcset
            srcset = tag.get('srcset')
            if srcset:
                parts = []
                for entry in srcset.split(','):
                    entry = entry.strip()
                    if not entry:
                        continue
                    subparts = entry.split()
                    if not subparts:
                        continue
                    img_url = subparts[0]
                    rewritten_img = rewrite_url(current_page_path, img_url)
                    if rewritten_img != img_url:
                        subparts[0] = rewritten_img
                    parts.append(" ".join(subparts))
                    # Add to assets
                    parsed = urllib.parse.urlparse(img_url)
                    if not parsed.netloc or parsed.netloc == "klusowski.princeton.edu":
                        norm_path = parsed.path if parsed.path else '/'
                        if norm_path not in LOCAL_PAGES:
                            discovered_assets.add(norm_path)
                tag['srcset'] = ", ".join(parts)
        elif tag.name in ['embed', 'object']:
            process_attr(tag, 'src')
            process_attr(tag, 'data')

    return str(soup)

def main():
    workspace = os.path.dirname(os.path.abspath(__file__))
    discovered_assets = set()
    html_contents = {}

    print("--- STEP 1: FETCHING AND REWRITING HTML PAGES ---")
    for page_path, rel_disk in LOCAL_PAGES.items():
        url = urllib.parse.urljoin(BASE_URL, page_path)
        print(f"Fetching page: {url}")
        try:
            response = requests.get(url, headers=BYPASS_HEADER)
            response.raise_for_status()
            html_contents[page_path] = response.text
        except Exception as e:
            print(f"FAILED to fetch page {url}: {e}")

    # Now rewrite and write pages to disk
    rewritten_pages = {}
    for page_path, raw_html in html_contents.items():
        print(f"Rewriting HTML for page: {page_path}")
        rewritten_pages[page_path] = rewrite_html(raw_html, page_path, discovered_assets)

    # Write HTML files to disk
    for page_path, html_str in rewritten_pages.items():
        rel_disk = LOCAL_PAGES[page_path]
        disk_path = os.path.join(workspace, rel_disk)
        os.makedirs(os.path.dirname(disk_path), exist_ok=True)
        with open(disk_path, 'w', encoding='utf-8') as f:
            f.write(html_str)
        print(f"Saved: {disk_path}")

    print("--- STEP 2: DOWNLOADING ASSETS ---")
    print(f"Found {len(discovered_assets)} unique assets to download.")
    for asset_path in sorted(discovered_assets):
        # Skip directories / blank paths / or external pages accidentally marked
        if not asset_path or asset_path == '/':
            continue
        # Construct local path on disk
        # Strip leading slash
        clean_asset = asset_path.lstrip('/')
        disk_path = os.path.join(workspace, clean_asset)
        
        # Download
        download_file(asset_path, disk_path)

    # Create .nojekyll
    nojekyll_path = os.path.join(workspace, ".nojekyll")
    with open(nojekyll_path, 'w') as f:
        pass
    print("Created .nojekyll file.")
    print("Mirroring complete!")

if __name__ == '__main__':
    main()
