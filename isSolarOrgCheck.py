import requests
from bs4 import BeautifulSoup
from googlesearch import search
import httpx
from prefect import task, flow

EXCLUDED_DOMAINS = [
    'facebook.com', 'linkedin.com', 'instagram.com', 'youtube.com', 'pinterest.com',
    'wikipedia.org', 'google.com', 'twitter.com', 'amazon.com', 'yelp.com',
    'tripadvisor.com', 'glassdoor.com', 'yellowpages.com'
]

# def get_org_name():
#     org_name = input("Enter the organization name: ")
#     return org_name

@task
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

@task
def check_solar_in_homepage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text().lower()
        return "solar" in text
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

@task
def call_webhook(payload):
    try:
        response = httpx.post("https://webhook.site/687e9031-fa94-43c1-86e6-001ac2dca609", json=payload)
        response.raise_for_status()
        return "yes"
    except httpx.HTTPStatusError:
        return "no"
    
@task
def update_hubspot(contact_id, org_name, is_solar, bearer_token):
    try:
        url = 'https://api.hubapi.com/crm/v3/objects/contacts/' + contact_id
        headers = {
            "authorization": "Bearer " + bearer_token
        }
        data = {
            "properties": {
                "is_solar": is_solar
            }
        }
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"HubSpot updated successfully for {org_name}")
        # return true
        return "yes"
         
    except Exception as e:
        print(f"An error occurred while updating HubSpot: {e}")
        return "no"

@flow(log_prints=True)
def isSolar(contact_id,org_name,bearer_token):
    # org_name = get_org_name()
    first_url = google_search(org_name)
    if first_url:
        print(f"First URL found: {first_url}")
        # result = check_solar_in_homepage(first_url)
        print(f"Is 'solar' present in the homepage? {result}")
        # update_hubspot_result = update_hubspot(contact_id, org_name, result, bearer_token)
        payload = {"company": org_name, "vid": contact_id, 
                   first_url: first_url,
                #    "isSolar": result,
                #    "updateHubSpot": update_hubspot_result
                   }
        resp = call_webhook(payload)
        
        
    else:
        print("No valid URL found in search results.")

if __name__ == "__main__":
    isSolar()
