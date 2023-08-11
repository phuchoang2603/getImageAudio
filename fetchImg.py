import openai
import requests
import time

# Set up your OpenAI API credentials
openai.api_key = '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'

# Set up the Imgbb API key
imgbb_api_key = 'e941bf827ee034be3d80c0d350f380be'

# Read the animal names from the input file
with open('input.txt', 'r') as file:
    inputFile = file.readlines()

# Generate images for each animal
for name in inputFile:
    name = name.strip()  # Remove any leading/trailing spaces or newlines
    prompt = f"an image of a {name}"
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    image_url = response['data'][0]['url']
    print(f"Generated image for {name}: {image_url}")
    
    # Upload the image to Imgbb
    upload_url = "https://api.imgbb.com/1/upload"
    params = {
        "key": imgbb_api_key,
        "image": image_url
    }
    response = requests.post(upload_url, params=params)
    json_response = response.json()
    if json_response['status'] == 200:
        image_url = json_response['data']['image']['url']
        print(f"Uploaded image for {name}: {image_url}")
    else:
        print(f"Error uploading image for {name}: {json_response['error']['message']}")

    # Wait 10 seconds to avoid hitting the rate limit
    time.sleep(10)
