import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def fetch_robots_txt():
    robots_url = "https://www.skatteverket.se/robots.txt"
    try:
        response = requests.get(robots_url)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
        return None

def parse_robots_txt(robots_txt):
    disallowed_paths = []
    user_agent = None

    for line in robots_txt.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Skip empty lines and comments
        if line.lower().startswith('user-agent'):
            user_agent = line.split(':', 1)[1].strip()
        elif line.lower().startswith('disallow') and user_agent == '*':
            path = line.split(':', 1)[1].strip()
            disallowed_paths.append(path)

    return disallowed_paths

def is_url_allowed(url, base_url, disallowed_paths):
    parsed_url = urlparse(url)
    path = parsed_url.path
    for disallowed_path in disallowed_paths:
        if path.startswith(disallowed_path):
            return False
    return True

def get_urls_from_directory(base_url, disallowed_paths, delay=1):
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all anchor tags
    anchor_tags = soup.find_all('a')

    # Extract the href attribute from each anchor tag
    urls = []
    for tag in anchor_tags:
        href = tag.get('href')
        if href:
            full_url = urljoin(base_url, href)  # Construct the full URL
            if full_url.startswith(base_url) and is_url_allowed(full_url, base_url, disallowed_paths):
                urls.append(full_url)

    # Introduce delay
    time.sleep(delay)

    return urls

# Usage
def __init__():
    base_url = "https://www.skatteverket.se/privat/folkbokforing/"
    robots_txt = fetch_robots_txt()
    if robots_txt:
        disallowed_paths = parse_robots_txt(robots_txt)
        urls = get_urls_from_directory(base_url, disallowed_paths, delay=1)

        for url in urls:
            print(url)
