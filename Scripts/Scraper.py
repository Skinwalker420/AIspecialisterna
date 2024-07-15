import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
from nltk.tokenize import sent_tokenize
import nltk.data
import json
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
    for url in urls:
        print(url)
    return urls

# Usage
def __init__():
    print("input website: ")
    base_url = input()
    robots_txt = fetch_robots_txt()
    if robots_txt:
        disallowed_paths = parse_robots_txt(robots_txt)
        urls = get_urls_from_directory(base_url, disallowed_paths, delay=1)

        for url in urls:
            scrape_page(url)


# Function to scrape a single page
def scrape_page(url):
    try:
        # Send HTTP GET request
        response = requests.get(url)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text content
            text_content = soup.get_text()

            # Save text content to a file
            
            clean(text_content)
        else:
            print(f'Error fetching URL: Status code {response.status_code}')

    except requests.RequestException as e:
        # Handle request exceptions (e.g., connection errors)
        print(f'Error fetching URL: {e}')

    except Exception as e:
        # Handle other exceptions
        print(f'Error: {e}')

def find_name(text):
    name = ""
    lines = [line for line in text.splitlines() if line.strip()]
    for i in lines[0]:
        if(i == "|"):
            name = name[:-1]
            break
        name += i
    print(name)
    return name

def clean(text):
    listeningFound = False
    kontaktFound = False
    nameFound = False
    name = find_name(text)
    lines = [line for line in text.splitlines() if line.strip()]
    textlength = len(lines)
    for i in range(textlength):
        if(lines[i] == "Lyssna"):
            lines[i] = ""
            listeningFound = True
        if(lines[i] == "Kontakta oss" and listeningFound):
            kontaktFound = True
        elif(listeningFound and lines[i] == name):
            nameFound = True
        if(not nameFound or kontaktFound):
            lines[i] = ""
    lines = [line for line in lines if line.strip()]
    separator = " "
    results = separator.join(lines)
    tokenize(results, name)

def tokenize(text, name):
        name = name.replace(' ', '')
        filePath = "/home/vinkemnt/Downloads/AIspecialisterna/AIspecialisterna/Dumps/" + name + ".json"
        tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
        sentences = sent_tokenize(text)
        # Output the sentences
        while(True):
            try:
                with open(filePath, 'w') as json_file:
                        json.dump(sentences, json_file, indent=4)
                        print(f"Data successfully saved to {filePath}")
                        break
            except:
                os.mkdir(filePath)

__init__()