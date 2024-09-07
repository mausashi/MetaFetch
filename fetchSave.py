import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin, urlsplit
import re

# Section 1
def fetch_url(url, output_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        filename = os.path.join(output_dir, f"{domain}.html")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        return response.text, filename, domain
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None, None

# Section 2
def collect_metadata(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    num_links = len(soup.find_all('a'))
    num_images = len(soup.find_all('img'))
    last_fetch = datetime.now(timezone.utc).strftime('%a %b %d %Y %H:%M UTC')
    return num_links, num_images, last_fetch

def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'[^\w\-_\. ]', '_', filename)  # Remove any other non-alphanumeric characters
    return filename

def strip_url_parameters(url):
    url_parts = urlsplit(url)
    return url_parts.path

# My attempt on Extra Credit
def download_assets(soup, base_url, domain, output_dir):
    assets = []
    for tag in soup.find_all(['img', 'script', 'link']):
        if tag.name == 'img' and tag.get('src'):
            assets.append((tag, 'src', tag['src']))
        elif tag.name == 'script' and tag.get('src'):
            assets.append((tag, 'src', tag['src']))
        elif tag.name == 'link' and tag.get('href'):
            assets.append((tag, 'href', tag['href']))

    asset_dir = os.path.join(output_dir, f"{domain}_assets")
    os.makedirs(asset_dir, exist_ok=True)

    for tag, attr, asset in assets:
        asset_url = urljoin(base_url, asset)
        sanitized_filename = sanitize_filename(os.path.basename(strip_url_parameters(asset_url)))
        asset_path = os.path.join(asset_dir, sanitized_filename)
        try:
            asset_response = requests.get(asset_url)
            asset_response.raise_for_status()
            with open(asset_path, 'wb') as asset_file:
                asset_file.write(asset_response.content)
            tag[attr] = os.path.join(asset_dir, sanitized_filename)
        except requests.RequestException as e:
            print(f"Error downloading asset {asset_url}: {e}")

# Main
def main():
    if len(sys.argv) < 2:
        print("Usage: ./fetchSave.py [--metadata] <url1> <url2> ...")
        return

    urls = sys.argv[1:]
    show_metadata = False

    if urls[0] == '--metadata':
        show_metadata = True
        urls = urls[1:]

    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)

    for url in urls:
        html_content, filename, domain = fetch_url(url, output_dir)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            download_assets(soup, url, domain, output_dir)
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            if show_metadata:
                num_links, num_images, last_fetch = collect_metadata(html_content)
                print(f"site: {filename}")
                print(f"num_links: {num_links}")
                print(f"images: {num_images}")
                print(f"last_fetch: {last_fetch}")

if __name__ == "__main__":
    main()