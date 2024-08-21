import requests
from prefect import task, flow
# from googlesearch import search
from datetime import datetime

EXCLUDED_DOMAINS = [
    'facebook.com', 'linkedin.com', 'instagram.com', 'youtube.com', 'pinterest.com',
    'wikipedia.org', 'google.com', 'twitter.com', 'amazon.com', 'yelp.com',
    'tripadvisor.com', 'glassdoor.com', 'yellowpages.com'
]
# import uuid
# @task
# def google_search(query):
#     search_url = f"https://www.google.com/search?q={query}"
#     print(f"Searching Google for: {query}")
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }
#     response = requests.get(search_url, headers=headers)
#     if response.status_code == 200:
#         # Manually parse the HTML to find the first URL
#         start_index = response.text.find('<a href="/url?q=') + len('<a href="/url?q=')
#         end_index = response.text.find('&amp;', start_index)
#         if start_index != -1 and end_index != -1:
#             return response.text[start_index:end_index]
#     return None
# @task
# def google_search(org_name):
#     try:
#         # Perform a Google search and get the first result
#         search_results = list(search(org_name, num_results=10))
#         for result in search_results:
#             if not any(domain in result for domain in EXCLUDED_DOMAINS):
#                 return result
#         return None
#     except Exception as e:
#         print(f"An error occurred during Google search: {e}")
#         return None

@task
def call_webhook(url, search_result):
    webhook_url = url

    payload = {
       "search_result": search_result
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, json=payload, headers=headers)
    return response.status_code, response.text

@flow(log_prints=True)
def isSolar(contact_id,org_name,bearer_token):
    fake = Faker()
        # Generate a fake name
    fake_name = fake.name()
    print(f"First fake name found: {fake_name}")
    status_code, response_text = call_webhook('https://webhook.site/687e9031-fa94-43c1-86e6-001ac2dca609', org_name+fake_name)
    print(f"Webhook response status: {status_code}")
    print(f"Webhook response text: {response_text}")
   

if __name__ == "__main__":
    isSolar()