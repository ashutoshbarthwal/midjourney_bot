import csv
import requests
import os

# Set the path to the CSV file
csv_path = '17022023.csv'

# Set the directory to save the downloaded images
save_dir = 'downloaded_images'

# Create the save directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# Open the CSV file
with open(csv_path, 'r') as f:
    reader = csv.reader(f)

    # Skip the header row if it exists
    next(reader, None)

    # Loop through the rows and download the images
    for i, row in enumerate(reader):
        image_url = row[2]
        response = requests.get(image_url)
        filename = os.path.join(save_dir, f'image_{i}.jpg')
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {image_url} and saved as {filename}')
