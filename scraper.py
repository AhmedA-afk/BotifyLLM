import requests
from bs4 import BeautifulSoup
import json  # Add this import statement

def scrape_webpage_structured(url):
    """
    Fetches and structures the content of a webpage.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        dict: A structured dictionary with webpage content.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.title.string if soup.title else "No Title Found"

        # Extract headings
        headings = {
            f"h{i}": [tag.get_text(strip=True) for tag in soup.find_all(f"h{i}")]
            for i in range(1, 7)  # From <h1> to <h6>
        }

        # Extract paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]

        # Extract metadata (description)
        meta_description = (
            soup.find("meta", attrs={"name": "description"}) or
            soup.find("meta", attrs={"property": "og:description"})
        )
        description = meta_description["content"] if meta_description else "No Description Found"

        # Compile the structured data
        structured_content = {
            "title": title,
            "description": description,
            "headings": headings,
            "paragraphs": paragraphs,
        }

        return structured_content

    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching webpage: {e}"}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

def update_json_file(file_name, new_data):
    """
    Updates the JSON file with new scraped data. If the file already exists,
    the new data will replace the old data.
    
    Args:
        file_name (str): The name of the JSON file.
        new_data (dict): The new data to save into the file.
    """
    try:
        # Save the new data to the JSON file
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        return {"status": "success", "message": "Data updated successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error updating JSON file: {e}"}
