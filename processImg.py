import openai
import requests
import time
import pandas as pd
from google.cloud import storage
from unidecode import unidecode
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

# Set up your OpenAI API credentials
openai.api_key = config['openai']['api_key']

# Set up Google Cloud Storage bucket information
bucket_name = config['google-cloud-storage']['bucket_name']

# Set up csv output file path
csv_output = config['csv']['output']

# Upload a file to a Google Cloud Storage bucket
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

# Function that generates the image for a given English word
def generate_image(word_en):
    prompt = f"an illustration of {word_en}"

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )

    image_url = response['data'][0]['url']

    return image_url

# Read the audio CSV file
df = pd.read_csv('audio.csv')

for index, row in df.iterrows():
    word_en = row['word_en'].lower()
    word_vn = row['word_vn']
    image_url = generate_image(word_en)

    print(f"Generated image for '{word_en}': {image_url}")

    # Download the image
    image_filename = f"{unidecode(word_vn).lower().replace(' ', '-').replace('/', '-')}.{word_en.lower()}.png"
    image_path = f"./image/{image_filename}"
    with open(image_path, 'wb') as f:
        f.write(requests.get(image_url).content)
    print(f"Saved image for '{word_en}' as {image_path}")

    # Upload the image to Google Cloud Storage
    upload_blob(bucket_name, image_path, "image/" + image_filename)
    print(f"Uploaded image for '{word_en}' to Google Cloud Storage.")

    # Get the image URL from the response and update the "image" column in the CSV file
    image_url = f"https://storage.googleapis.com/{bucket_name}/image/{image_filename}"
    df.at[index, 'image'] = image_url
    print (f"Updated image URL for '{word_en}' to {image_url}")

    # Wait 5 seconds before making the next API call
    time.sleep(5)

# Save the updated CSV file
df.to_csv(csv_output, index=False)
