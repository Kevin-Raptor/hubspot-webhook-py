import requests
from bs4 import BeautifulSoup
from googlesearch import search
import httpx

import logging

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
        print(response)
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup)
        text = soup.get_text().lower()
        print(text)
        return "solar" in text
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def call_webhook(payload):
    try:
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dictionary")
        response = httpx.post("https://webhook.site/687e9031-fa94-43c1-86e6-001ac2dca609", json=payload)
        response.raise_for_status()
        return True
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        logging.error(f"HTTP error occurred: {e}")
        return False
    except ValueError as e:
        logging.error(f"Value error: {e}")
        return False

    
def update_hubspot(contact_id, org_name, is_solar):
    try:
        if not isinstance(contact_id, int):
            raise ValueError("Contact ID must be an integer")
        if not org_name or not isinstance(org_name, str):
            raise ValueError("Organization name must be a non-empty string")
        if not isinstance(is_solar, bool):
            raise ValueError("is_solar must be a boolean")

        url = f'https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}'
        headers = {
            "authorization": "Bearer abc"
        }
        data = {
            "properties": {
                "is_solar": is_solar
            }
        }
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"HubSpot updated successfully for {org_name}")
        return True
    except (requests.HTTPError, requests.RequestException) as e:
        logging.error(f"HTTP error occurred: {e}")
        return False
    except ValueError as e:
        logging.error(f"Value error: {e}")
        return False

def isSolarOrgCheck(contact_id,org_name):
    # org_name = get_org_name()
    first_url = google_search(org_name)
    if first_url:
        print(f"First URL found: {first_url}")
        result = check_solar_in_homepage(first_url)
        print(f"Is 'solar' present in the homepage? {result}")
        update_hubspot_result = update_hubspot(contact_id, org_name, result)
        payload = {"company": org_name, "vid": contact_id, "isSolar": result, "updateHubSpot": update_hubspot_result}
        resp = call_webhook(payload)
        
    else:
        print("No valid URL found in search results.")

if __name__ == "__main__":
    isSolarOrgCheck(45686033552, 'Solaria')