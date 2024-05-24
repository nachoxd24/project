import requests

API_URL = "https://www.stack-ai.com/internal_ui/4e57104a-ef26-4eac-b479-5a09cbb5becd/acf2ae74-478a-444a-923f-d2e56b5c5eff/64e62c505c4ed0a524c8eb08"
headers = {'Authorization':
			 'Bearer acfc30e7-fe6b-444e-bf09-fc154d01b530',
			 'Content-Type': 'application/json'
		}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({"in-0": "cuando fue la segunda guerra mundial", "user_id": ""})
print(output)