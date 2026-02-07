import requests
from pprint import pprint

# Test the CORS headers on the backend
url = "http://localhost:8000/health"

# Make a preflight request (OPTIONS) to check CORS headers
preflight_response = requests.options(url, headers={
    "Origin": "http://localhost:3000",
    "Access-Control-Request-Method": "GET",
    "Access-Control-Request-Headers": "X-Requested-With, Content-Type"
})

print("Preflight (OPTIONS) Response Headers:")
pprint(dict(preflight_response.headers))

print("\nActual GET Request Headers:")
get_response = requests.get(url)
pprint(dict(get_response.headers))