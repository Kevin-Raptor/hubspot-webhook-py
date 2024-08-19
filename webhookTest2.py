import httpx
from prefect import task, flow

@task
def call_webhook(url, payload):
    try:
        response = httpx.post(url, json=payload)
        response.raise_for_status()
        return "yes"
    except httpx.HTTPStatusError:
        return "no"
    
@flow(log_prints=True)
def hs_webhook(name, vid):
    url = "https://webhook.site/ed1c1eb5-6e05-4358-a8b6-a8f3cfdd030e"
    payload = {"company": name}
    payload = {"vid": vid}
    resp = call_webhook(url, payload)
    print('~~~~~~~~response is ' + resp + 'for ' + name)



if __name__ == "__main__":
    hs_webhook()