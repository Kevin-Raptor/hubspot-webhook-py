from datetime import datetime
from faker import Faker

EXCLUDED_DOMAINS = ["example.com", "anotherexample.com"]

def test_faker():
    try:
        # Create a Faker instance
        fake = Faker()
        # Generate a fake name
        fake_name = fake.name()
        print(f"Generated fake name: {fake_name}")
    except Exception as e:
        print(f"An error occurred while testing the faker library: {e}")

# Run the test function
test_faker()