import requests
import json
import pandas as pd
from google.cloud import storage
from unidecode import unidecode
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

# Set up the Viettel API key
viettel_api_key = config['viettel-ai']['api_key']

# Set up Google Cloud Storage bucket information
bucket_name = config['google-cloud-storage']['bucket_name']

# Set up csv input file path
csv_input = config['csv']['input']

# Function that uploads a file to a Google Cloud Storage bucket
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

# Function that generates the audio file for a given Vietnamese word
def generate_audio(word_vn):
    payload = json.dumps({
        "text": word_vn,
        "voice": "hn-thaochi",
        "speed": 0.7,
        "tts_return_option": 2,
        "token": viettel_api_key,
        "without_filter": False
    })

    headers = {'accept': '*/*','Content-Type': 'application/json'}

    # Make the Viettel API call
    response = requests.post(url="https://viettelai.vn/tts/speech_synthesis", headers=headers, data=payload)

    return response

# Get the data from the CSV file
df = pd.read_csv(csv_input)

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    word_vn = row['word_vn']
    word_en = row['word_en']
    
    # Save the audio file
    audio_filename = f"{unidecode(word_vn).lower().replace(' ', '-').replace('/', '-')}.{word_en.lower()}.wav"
    audio_path = f"./audio/{audio_filename}"
    with open(audio_path, 'wb') as f:
        f.write(generate_audio(word_vn).content)
    print(f"Saved audio for '{word_en}' as {audio_path}")

    # Upload the audio file to Google Cloud Storage
    upload_blob(bucket_name, audio_path, "audio/" + audio_filename)
    print(f"Uploaded audio for '{word_en}' to Google Cloud Storage.")

    # Get the audio URL from the response and update the "pronunciation" column in the CSV file
    audio_url = f"https://storage.googleapis.com/{bucket_name}/audio/{audio_filename}"
    df.at[index, 'pronunciation'] = audio_url
    print(f"Updated 'pronunciation' column for '{word_en}' with audio URL: {audio_url}")


# Save the updated DataFrame back to the CSV file
df.to_csv('audio.csv', index=False)