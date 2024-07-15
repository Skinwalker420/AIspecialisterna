import requests
from bs4 import BeautifulSoup

def scrape_website(url, output_file):
    try:
        # Send HTTP GET request
        response = requests.get(url)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract all text from the page
            text_content = soup.get_text()

            # Write text content to a file
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(text_content)

            print(f'Successfully scraped and saved text to {output_file}')

        else:
            print(f'Error fetching URL: Status code {response.status_code}')

    except requests.RequestException as e:
        # Handle request exceptions (e.g., connection errors)
        print(f'Error fetching URL: {e}')

    except Exception as e:
        # Handle other exceptions
        print(f'Error: {e}')

if __name__ == "__main__":
    url = 'https://skatteverket.se/privat/folkbokforing.4.18e1b10334ebe8bc800039.html'  # Replace with the URL of the website you want to scrape
    output_file = 'skatten_text.txt'  # Replace with the desired output file path

    scrape_website(url, output_file)

