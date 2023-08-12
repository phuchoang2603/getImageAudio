# Text to Image and Speech batch processing

This project generates images based on text prompts using the OpenAI API and converts text to speech using the ViettelAI API. The generated images are then uploaded to Google Cloud Storage and the corresponding URLs are added back to the CSV file.

## Prerequisites

- Python 3 installed on your machine
- OpenAI Python library (`openai`) installed (`pip install openai`)
- Google Cloud Storage Python library (`google-cloud-storage`) installed (`pip install google-cloud-storage`) and configured (see [Setup](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev))

## Setup

1. Clone this repository to your local machine:

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate.bat  # For Windows
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Obtain API keys:
   - OpenAI API: Follow the instructions in the [OpenAI documentation](https://platform.openai.com/docs/guides/images) to obtain your API key and add it to the `config.ini` file in the `[open-ai]` section.
   - ViettelAI API: Follow the instructions in the [ViettelAI documentation](https://viettelgroup.ai/document/tts) to obtain your API key and add it to the `config.ini` file in the `[viettel-ai]` section.
   - Google Cloud Storage: Follow the instructions in the [Google Cloud Storage documentation](https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-client-libraries) to set up your Storage bucket and obtain the necessary credentials. Add the bucket name to the `config.ini` file in the `[bucket-name]` section.

## Usage

1. Prepare your CSV file:
   - Create a CSV file with the desired column names.
   - Add your input data, including the English words, Vietnamese words, and pronunciations.
   - Save the file with the desired name (e.g., `cards.csv`) and update the `config.ini` file in the `[input-file]` section with the file name.

2. Run the Python script for image generation:
   ```
   python main.py
   ```

   This script will 
   - read the data from the CSV file specified in the `config.ini` file (e.g., `cards.csv`)
   - convert the English words to speech using the ViettelAI API, and save the audio files locally.
   - generate images for the English words using the OpenAI API, and save the images locally.
   - upload the audio and image files to Google Cloud Storage.
   - update the CSV file with the URLs of the generated images and the paths to the converted audio files.

3. Check the updated CSV file:
   - After running the script, open the output CSV file specified in the `config.ini` file (e.g., `final.csv`) to see the updated information.
   - The `image_url` column will contain the URLs of the generated images, and the `audio_file` column will contain the paths to the converted audio files.