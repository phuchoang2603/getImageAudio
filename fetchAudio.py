import requests
import json
from google.cloud import storage

url = "https://viettelai.vn/tts/speech_synthesis"
viettel_api_key = '78513ac98aba28746c6726732b0510b5'

payload = json.dumps({
"text": "Văn bản cần đọc",
"voice": "hn-thaochi",
"speed": 0.7,
"tts_return_option": 2,
"token": viettel_api_key,
"without_filter": False
})

headers = {
'accept': '*/*',
'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)