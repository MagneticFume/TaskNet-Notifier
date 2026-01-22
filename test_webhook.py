import requests
import json
import sys

# Default to localhost:5000
port = 5000
if len(sys.argv) > 1:
    port = int(sys.argv[1])

url = f"http://localhost:{port}/webhook"
payload = {
    "title": "Fix the header bug",
    "description": "The logo is not aligning correctly on mobile devices.",
    "url": "https://yourwebsite.com/tasks/123"
}

headers = {'Content-Type': 'application/json'}

print(f"Sending test webhook to {url}...")
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Response Content: {response.text}")
except Exception as e:
    print(f"Error: {e}")
