import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('./csv-files/cards.csv')

# Define the columns to convert to lowercase
columns_to_lowercase = ["word_vn", "word_en", "word_fr", "starting_letter"]

# Loop through each row and convert the specified columns to lowercase
for column in columns_to_lowercase:
    df[column] = df[column].str.lower()

# Save the modified DataFrame back to a CSV file
df.to_csv('./csv-files/lowercase.csv', index=False)