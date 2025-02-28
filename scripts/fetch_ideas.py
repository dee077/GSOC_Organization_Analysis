import os
import requests
from dotenv import load_dotenv

load_dotenv()

# SerpApi configuration
SERPAPI_API_KEY = os.getenv("SERPAPI_KEY")
SEARCH_ENGINE = "google"  # You can use other search engines too like bing, yahoo

org_name = "Openwisp"  # Your organization's name

def construct_query(org_name):
    """Construct the search query to find GSoC 2024 project ideas for the given organization."""
    return f"Find the official project ideas list for '{org_name}' and make sure it is for '{org_name}' and the number of project ideas available for the organization '{org_name}' in GSoC 2024. Provide the exact link to the project ideas list page for {org_name}, along with the number of project ideas available. Return the result as an object: {{'no_of_ideas': <count>, 'link': <url>}}"


def fetch_project_ideas_and_count(org_name):
    """Fetch project ideas and count for a given organization using SerpApi."""
    query = construct_query(org_name)
    params = {
        'q': query,
        'api_key': SERPAPI_API_KEY,
        'engine': SEARCH_ENGINE
    }
    
    try:
        # Send the request to SerpApi
        response = requests.get("https://serpapi.com/search", params=params)
        response_data = response.json()

        # Check for 'organic_results' in the response
        if 'organic_results' in response_data:
            # Extract relevant information (link and number of ideas)
            ideas_link = None
            num_ideas = 0
            for result in response_data['organic_results']:
                if 'title' in result and 'gsoc' in result['title'].lower():
                    ideas_link = result.get('link')
                    num_ideas += 1
            
            return ideas_link, num_ideas
        else:
            print("No relevant results found.")
            return None, None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None

if __name__ == "__main__":
    print(f"Fetching project ideas and count for organization: {org_name}")
    link, num_ideas = fetch_project_ideas_and_count(org_name)

    if link and num_ideas:
        print(f"Project Ideas Link: {link}")
        print(f"Number of Ideas: {num_ideas}")
    else:
        print("Failed to fetch or parse project ideas and count.")
