import requests
from prefect import flow

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        # Manually parse the HTML to find the first URL
        start_index = response.text.find('<a href="/url?q=') + len('<a href="/url?q=')
        end_index = response.text.find('&amp;', start_index)
        if start_index != -1 and end_index != -1:
            return response.text[start_index:end_index]
    return None

def check_solar_in_homepage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return "solar" in response.text.lower()
    return False

def update_hubspot(contact_id, org_name, result, bearer_token):
    # Dummy implementation for updating HubSpot
    try:
        # Simulate an API call to update HubSpot
        print(f"Updating HubSpot for contact_id: {contact_id}, org_name: {org_name}, result: {result}")
        return "success"
    except Exception as e:
        print(f"An error occurred while updating HubSpot: {e}")
        return "no"

@flow(log_prints=True)
def isSolar(contact_id, org_name, bearer_token):
    first_url = google_search(org_name)
    if first_url:
        print(f"First URL found: {first_url}")
        result = check_solar_in_homepage(first_url)
        print(f"Is 'solar' present in the homepage? {result}")
        # update_hubspot_result = update_hubspot(contact_id, org_name, result, bearer_token)
        payload = {
            "company": org_name,
            "vid": contact_id,
            "first_url": first_url,
            "isSolar": result,
            # "updateHubSpot": update_hubspot_result
        }
        print(f"Payload: {payload}")
        return payload
    else:
        print("No URL found")
        return None

if __name__ == "__main__":
    # Example usage
    # contact_id = "12345"
    # org_name = "Arka energy"
    # bearer_token = "your_bearer_token"
    isSolar()