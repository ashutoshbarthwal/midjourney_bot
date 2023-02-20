import requests
from bs4 import BeautifulSoup
import os

# Set the URL of the recent showcase page
url = 'https://www.midjourney.com/showcase/recent/'

# Send a request to the page
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

print(soup)

# Find all the image tags on the page
images = soup.find_all('img')

print(images)

# Create a directory to store the downloaded images
os.makedirs('midjourney_images', exist_ok=True)

# # Download each image and save it to the directory
# for i, image in enumerate(images):
#     image_url = image.get('src')
#     if image_url:
#         response = requests.get(image_url)
#         filename = f'midjourney_images/image{i}.jpg'
#         with open(filename, 'wb') as f:
#             f.write(response.content)
#         print(f'Saved {filename}')
