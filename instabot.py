import os
import random
from instabot import Bot

# Set the username and password for the Instagram account
username = 'your_instagram_username'
password = 'your_instagram_password'

# Set the path to the folder with the images to post
image_folder = 'path/to/images/folder'

# Create a new instance of the InstaBot class
bot = Bot()

# Login to the Instagram account
bot.login(username=username, password=password)

# Get a list of the image files in the folder
image_files = os.listdir(image_folder)

# Choose a random image file from the folder
image_file = random.choice(image_files)

# Set the caption for the post
caption = 'This is my automated Instagram post!'

# Post the image and caption to Instagram
bot.upload_photo(os.path.join(image_folder, image_file), caption=caption)

# Logout of the Instagram account
bot.logout()
