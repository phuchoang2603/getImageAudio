import pandas as pd
import os

# Define the path to the CSV file and image folder
csv_file = './csv-files/lowercase.csv'  # Replace with your CSV file path
image_folder = 'image'  # Replace with your image folder path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    word_en = row['word_en']  # Get the value in the "word_en" column
    
    # Construct the image file path based on the "word_en" name
    image_path = os.path.join(image_folder, f'{word_en}.jpg')  # Assumes image file format is jpg
    
    # Check if the image file not exists
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
