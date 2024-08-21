import requests
from prefect import task, flow

@task
def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    print(f"Searching Google for: {query}")
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
    first_url = google_search(org_name)
    if first_url:
        print(f"First URL found: {first_url}")
        status_code, response_text = call_webhook('https://webhook.site/687e9031-fa94-43c1-86e6-001ac2dca609', first_url)
        print(f"Webhook response status: {status_code}")
        print(f"Webhook response text: {response_text}")
    else:
        print("No URL found")

if __name__ == "__main__":
    contact_id = 123
    org_name = "Solar Energy Inc."
    bearer ='asd'
    isSolar(contact_id,org_name,bearer)