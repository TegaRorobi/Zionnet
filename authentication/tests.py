from django.test import TestCase

# Create your tests here.
import requests

data = {
    "email": "",
    "first_name": "muhammed",
    "last_name": "yuguda",
    "phone_number": 12388899,
    "country": "niger",
    'password': 21838345
}
response = requests.post('http://127.0.0.1:8000/auth/register/', data = data)

print(response.json())