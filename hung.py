import requests

API_URL = "https://api-inference.huggingface.co/models/VietAI/gpt-neo-1.3B-vietnamese-news"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Sơ cứu khi bị ong đốt",
})
print(output)