import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_google_search_results(search_query):
    url = f"https://www.google.com/search?q={requests.utils.quote(search_query + ' company')}"
    print('Google search URL:', url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        print('Response:', response.text)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        excluded_domains = [
            'facebook.com', 'linkedin.com', 'instagram.com', 'youtube.com', 'pinterest.com', 
            'wikipedia.org', 'google.com', 'twitter.com', 'amazon.com', 'yelp.com', 
            'tripadvisor.com', 'glassdoor.com', 'yellowpages.com'
        ]
        # print('soup:', soup)

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/url?'):
                url_params = parse_qs(urlparse(href).query)
                actual_url = url_params.get('q', [None])[0]
                if actual_url and actual_url.startswith('https://'):
                    domain = urlparse(actual_url).hostname
                    if not any(excluded_domain in domain for excluded_domain in excluded_domains):
                        links.append(actual_url)
        return links
    except requests.RequestException as e:
        print('Error fetching the Google search results:', e)
        return []

def check_is_solar(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()
        return 'solar' in text
    except requests.RequestException as e:
        print('Error fetching the URL:', e)
        return False

def is_solar_checker(search_query):
    links = get_google_search_results(search_query)
    print('Filtered HTTPS URLs from Google search results:', links)
    results = []
    for url in links[:2]:
        is_solar = check_is_solar(url)
        results.append({'url': url, 'is_solar': is_solar})
    return results

def main_function():
    search_query = 'arka'
    results = is_solar_checker(search_query)
    print('Results:', results)

if __name__ == "__main__":
    main_function()