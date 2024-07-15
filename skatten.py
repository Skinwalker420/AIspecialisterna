import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

# Function to scrape a single page
def scrape_page(url, output_folder, visited_pages):
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
            filename = os.path.join(output_folder, f'{urlparse(url).path.strip("/").replace("/", "_")}.txt')
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text_content)

            print(f'Successfully scraped and saved text to {filename}')

            # Extract all links (a tags) from the page
            links = soup.find_all('a', href=True)
            for link in links:
                # Construct absolute URL
                next_url = urljoin(url, link['href'])
                # Check if it belongs to the same directory
                if next_url.startswith(url) and next_url not in visited_pages:
                    # Add to visited pages to avoid duplicates
                    visited_pages.add(next_url)
                    # Recursive call to scrape next page
                    scrape_page(next_url, output_folder, visited_pages)

        else:
            print(f'Error fetching URL: Status code {response.status_code}')

    except requests.RequestException as e:
        # Handle request exceptions (e.g., connection errors)
        print(f'Error fetching URL: {e}')

    except Exception as e:
        # Handle other exceptions
        print(f'Error: {e}')

if __name__ == "__main__":
    starting_url = 'https://skatteverket.se/privat/folkbokforing'  # Replace with the URL of the starting directory
    output_folder = 'scraped_pages'  # Replace with the desired output folder path

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize set to keep track of visited pages
    visited_pages = set()
    visited_pages.add(starting_url)

    # Start scraping from the starting URL
    scrape_page(starting_url, output_folder, visited_pages)
