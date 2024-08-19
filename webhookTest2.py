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
    url = "https://webhook.site/687e9031-fa94-43c1-86e6-001ac2dca609"
    payload = {"company": name}
    payload = {"vid": vid}
    resp = call_webhook(url, payload)
    print('~~~~~~~~response is ' + resp + 'for ' + name)



if __name__ == "__main__":
    hs_webhook()