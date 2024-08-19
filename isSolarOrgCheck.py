import requests
from bs4 import BeautifulSoup
from googlesearch import search

EXCLUDED_DOMAINS = [
    'facebook.com', 'linkedin.com', 'instagram.com', 'youtube.com', 'pinterest.com',
    'wikipedia.org', 'google.com', 'twitter.com', 'amazon.com', 'yelp.com',
    'tripadvisor.com', 'glassdoor.com', 'yellowpages.com'
]

# def get_org_name():
#     org_name = input("Enter the organization name: ")
#     return org_name

def google_search(org_name):
    try:
        # Perform a Google search and get the first result
        search_results = list(search(org_name, num_results=10))
        for result in search_results:
            if not any(domain in result for domain in EXCLUDED_DOMAINS):
                return result
        return None
    except Exception as e:
        print(f"An error occurred during Google search: {e}")
        return None

def check_solar_in_homepage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text().lower()
        return "solar" in text
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def isSolarOrgCheck(contact_id,org_name):
    # org_name = get_org_name()
    first_url = google_search(org_name)
    if first_url:
        print(f"First URL found: {first_url}")
        result = check_solar_in_homepage(first_url)
        print(f"Is 'solar' present in the homepage? {result}")
    else:
        print("No valid URL found in search results.")

if __name__ == "__main__":
    isSolarOrgCheck()