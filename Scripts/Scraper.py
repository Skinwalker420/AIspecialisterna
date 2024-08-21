import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
from nltk.tokenize import sent_tokenize
import nltk.data
import nltk
import json
import time
import re

visited_urls = set()

def exitPrompt():
    input('Press ENTER to exit')

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

def is_url_allowed(url, disallowed_paths):
    parsed_url = urlparse(url)
    path = parsed_url.path
    for disallowed_path in disallowed_paths:
        if path.startswith(disallowed_path):
            return False
    return True

def get_urls_from_directory(url, disallowed_paths, delay=1):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all anchor tags
    anchor_tags = soup.find_all('a')

    # Extract the href attribute from each anchor tag
    urls = []
    for tag in anchor_tags:
        href = tag.get('href')
        if href:
            full_url = urljoin(url, href) # Construct the full URL
            if full_url.startswith(base_url) and is_url_allowed(full_url, disallowed_paths) and full_url not in visited_urls and '#' not in full_url:
                visited_urls.add(full_url)
                urls.append(full_url)
                print(full_url)
                print('visited pages: ' + str(len(visited_urls)))
    # Introduce delay
    time.sleep(delay)
    return urls

def crawl(url, disallowed_paths):
    try:
        links = get_urls_from_directory(url, disallowed_paths)
        for link in links:
            print(link)
            crawl(link, disallowed_paths)
    except Exception as e:
        print(e)

        
# Usage
def __init__():
    print("input website: ")
    global file_path
    global base_url
    global full_file
    full_file = []
    base_url = input()
    print("file path: ")
    file_path = input()
    print("file name: ")
    name = input()
    robots_txt = fetch_robots_txt()
    file_path = file_path + '/' + name + ".json"
    if robots_txt:
        disallowed_paths = parse_robots_txt(robots_txt)
        crawl(base_url, disallowed_paths)

        for url in visited_urls:
            scrape_page(url)

    while(True):
            try:
                with open(file_path, 'w') as json_file:
                        json.dump(full_file, json_file, indent=4)
                        print(f"Data successfully saved to {file_path}")
                        break
            except:
                os.mkdir(file_path)
    print("finished. Press enter to exit")
    input()


# Function to scrape a single page
def scrape_page(url):
    try:
        # Send HTTP GET request
        response = requests.get(url)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(response.content, "lxml")
            elements = soup.find_all('p')
            title = soup.find('title')
            
            name = find_name(title)

            # Extract text content
            text_content = []

            for element in elements:
                if element.find('a'):
                    continue
                text_content.append(element.get_text(strip = True))
            text_content = text_content[:-2]
            full_text = ' '.join(text_content)
            
            tokenize(full_text, name, url)
        else:
            print(f'Error fetching URL: Status code {response.status_code}')

    except requests.RequestException as e:
        # Handle request exceptions (e.g., connection errors)
        print(f'Error fetching URL: {e}')

    except Exception as e:
        # Handle other exceptions
        print(f'Error: {e}')

def find_name(title):
    name = ""
    title = BeautifulSoup.get_text(title)
    for i in title:
        if(i == "|"):
            name = name[:-1]
            break
        name += i
    name = name.replace('/', '-')
    name = name.replace(':', "-")
    print(name)
    return name

def tokenize(text, name, url):
        name = name.replace(' ', '')
        tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
        sentences = sent_tokenize(text)
        # Output the sentences
        full_file.append(url)
        full_file.append(sentences)

        # while(True):
        #     try:
        #         with open(filePath, 'w') as json_file:
        #                 json.dump(sentences, json_file, indent=4)
        #                 print(f"Data successfully saved to {filePath}")
        #                 break
        #     except:
        #         os.mkdir(filePath)

__init__()

