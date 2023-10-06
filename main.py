import openai
import requests
import json
import time
import pandas as pd
from google.cloud import storage
from unidecode import unidecode
from configparser import ConfigParser
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the Viettel API key
config = ConfigParser()
config.read('config.ini')
viettel_api_key = config.get('viettel-ai', 'api_key')

# Function that uploads a file to a Google Cloud Storage bucket
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    logging.info(f"File {source_file_name} uploaded to {destination_blob_name}.")

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

# Function that generates the image for a given English word
def generate_image(word_en):
    prompt = f"{word_en}, digital art, brown background"

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )

    image_url = response['data'][0]['url']

    return image_url

# Main program
def main():
    # Set up your OpenAI API credentials
    # openai.api_key = config.get('open-ai', 'api_key')

    # Set up Google Cloud Storage bucket information
    bucket_name = config.get('google-cloud-storage', 'bucket_name')

    # Set up csv input file path
    csv_input = config.get('csv-file', 'input')

    # Set up csv output file path
    csv_output = config.get('csv-file', 'output')

    # Get the data from the CSV file
    df = pd.read_csv(csv_input)

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        word_vn = row['word_vn']
        word_en = row['word_en']
        file_name = word_en
        
        try:
            # Generate the audio file for the Vietnamese word
            audio_response = generate_audio(word_vn)
            if audio_response.status_code == 200:
                audio_path = os.path.join('audio', f"{file_name}.wav")
                with open(audio_path, 'wb') as f:
                    f.write(audio_response.content)
                logging.info(f"Saved audio for '{word_en}' as {audio_path}")
            else:
                logging.error(f"Failed to generate audio for '{word_en}'. Status code: {audio_response.status_code}")

            # Generate the image for the English word
            # image_url = generate_image(word_en)
            # logging.info(f"Generated image for '{word_en}': {image_url}")
            # image_filename = f"{file_name}.png"
            # image_path = os.path.join('image', image_filename)
            # image_response = requests.get(image_url)
            # if image_response.status_code == 200:
            #     with open(image_path, 'wb') as f:
            #         f.write(image_response.content)
            #     logging.info(f"Saved image for '{word_en}' as {image_path}")
            # else:
            #     logging.error(f"Failed to generate image for '{word_en}'. Status code: {image_response.status_code}")

            # Upload the audio file to Google Cloud Storage
            upload_blob(bucket_name, audio_path, 'audio/' + file_name)
            logging.info(f"Uploaded audio for '{word_en}' to Google Cloud Storage.")

            # Upload the image to Google Cloud Storage
            image_path = os.path.join('image', f"{file_name}.jpg")
            upload_blob(bucket_name, image_path, 'image/' + file_name)
            logging.info(f"Uploaded image for '{word_en}' to Google Cloud Storage.")

            # Get the audio URL and image_url from the response and update the "pronunciation" and "image" column in the CSV file respectively
            audio_url = f"https://storage.googleapis.com/{bucket_name}/audio/{file_name}"
            image_url = f"https://storage.googleapis.com/{bucket_name}/image/{file_name}"
            df.at[index, 'pronunciation'] = audio_url
            df.at[index, 'image'] = image_url

            # Logging the urls for images and audio
            logging.info(f"Audio URL: {audio_url}")
            logging.info(f"Image URL: {image_url}")            
        except Exception as e:
            logging.error(f"Error processing word '{word_en}': {e}")

        # Delay for 5 seconds to avoid hitting the OpenAI API rate limit
        # logging.info("Waiting 5 seconds to avoid hitting the OpenAI API rate limit...")
        # time.sleep(5)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_output, index=False)
    logging.info(f"Saved updated DataFrame to {csv_output}.")


# Run the main program
if __name__ == "__main__":
    main()