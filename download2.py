from selenium import webdriver
import os
import time

# Set the URL of the page with the images
url = 'https://www.midjourney.com/showcase/recent/'

# Create a new Chrome browser instance
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

# Load the page
driver.get(url)

# Wait for the images to load
time.sleep(5)

# Find the element that contains the images
image_container = driver.find_element_by_css_selector('.image-container')

# Find all the image elements inside the container
images = driver.find_elements_by_tag_name('img')

# Create a directory to store the downloaded images
os.makedirs('downloaded_images', exist_ok=True)

# Download each image and save it to the directory
for i, image in enumerate(images):
    image_url = image.get_attribute('src')
    if image_url:
        response = requests.get(image_url)
        filename = f'downloaded_images/image{i}.jpg'
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Saved {filename}')

# Close the browser
driver.quit()
