

from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/Kevin-Raptor/hubspot-webhook-py.git",
        entrypoint="webhookTest.py:hit_webhook",
    ).deploy(
        name="my-first-deployment",
        work_pool_name="my-managed-pool",
        parameters={"param1": "value1", "param2": "value2"}
    )