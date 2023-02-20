import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import re
from concurrent.futures import ThreadPoolExecutor

def check_file_exists_else_create(file_path,filename,data,mode='w'):
    if os.path.exists(file_path+'/'+filename) and os.path.isfile(file_path+'/'+filename):
        print('File already exists.')
    else:
        with open(file_path+'/'+filename, mode) as f:
            f.write(data)
        print(f'Downloaded variable {file_path} and saved as {filename}')

# Get current datetime
now = datetime.now()

# Set the URL of the webpage with the JSON object in a script tag
url = 'https://www.midjourney.com/showcase/recent/'

# Make a request to the webpage and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the script tag with an id of '__NEXT_DATA__' and get its contents
script = soup.find('script', {'id': '__NEXT_DATA__'})
json_string = script.contents[0]

# Parse the JSON string into a Python object
json_object = json.loads(json_string)

# Format datetime as 'YYYYMMDD'
directory = now.strftime('%Y%m%d')

# Create the save directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Specify output file name
output_file = directory+'/response.json'

check_file_exists_else_create(directory,'response.json',json_string)

# if os.path.exists(output_file) and os.path.isfile(output_file):
#             print('File already exists.')
# else:
#     # Write data to output file
#     with open(output_file, 'w') as f:
#         json.dump(json_object, f)



def processRecord(record):
    print("Processing record: "+record['id'])
    main_path = directory+'/'+record['id']+'/main'
    os.makedirs(main_path, exist_ok=True)
    for image_url in record['image_paths']:
        response = requests.get(image_url)
        image_name = image_url.split('/')
        filename = os.path.join(main_path, image_name[-1])
        check_file_exists_else_create(main_path,image_name[-1],response.content,mode='wb')
    
    variations = directory+'/'+record['id']+'/'+record['event']['eventType']
    os.makedirs(variations, exist_ok=True)
    image_path = record['event']["seedImageURL"]

    for i in range(4):
        var_image_name = '0_'+str(i)+'.png'
        var_image_path = re.sub(r'0_[0-9].png',var_image_name , image_path)
        response = requests.get(var_image_path)
        filename = os.path.join(variations, var_image_name)
        check_file_exists_else_create(variations,var_image_name,response.content,'wb')
    
    check_file_exists_else_create(main_path,'promt.txt',record['prompt'])
    check_file_exists_else_create(main_path,'record.json',json.dumps(record))

# Access the desired data from the JSON object
data = json_object['props']['pageProps']['jobs']


# Create a thread pool with a maximum of 4 threads
with ThreadPoolExecutor(max_workers=20) as executor:
    # Submit each download task to the thread pool
    futures = [executor.submit(processRecord, record) for record in data]
    
    # Wait for all tasks to complete
    for future in futures:
        future.result()

# for record in data:
#     processRecord(record)

# for record in data:
#     main_path = directory+'/'+record['id']+'/main'
#     os.makedirs(main_path, exist_ok=True)
#     for image_url in record['image_paths']:
#         response = requests.get(image_url)
#         image_name = image_url.split('/')
#         filename = os.path.join(main_path, image_name[-1])
#         check_file_exists_else_create(main_path,image_name[-1],response.content,mode='wb')
#         # if os.path.exists(filename) and os.path.isfile(filename):
#         #     print('File already exists.')
#         # else:
#         #     print('File does not exist.')
#         #     with open(filename, 'wb') as f:
#         #         f.write(response.content)
#         #     print(f'Downloaded main image {image_url} and saved as {filename}')
    
#     variations = directory+'/'+record['id']+'/'+record['event']['eventType']
#     os.makedirs(variations, exist_ok=True)
#     image_path = record['event']["seedImageURL"]

#     for i in range(4):
#         var_image_name = '0_'+str(i)+'.png'
#         var_image_path = re.sub(r'0_[0-9].png',var_image_name , image_path)
#         response = requests.get(var_image_path)
#         filename = os.path.join(variations, var_image_name)
#         check_file_exists_else_create(variations,var_image_name,response.content,'wb')
#         # if os.path.exists(filename) and os.path.isfile(filename):
#         #     print('File already exists.')
#         # else:
#         #     with open(filename, 'wb') as f:
#         #         f.write(response.content)
#         #     print(f'Downloaded variable {var_image_path} and saved as {filename}')
    
#     check_file_exists_else_create(main_path,'promt.txt',record['prompt'])
#     # if os.path.exists(main_path+'/promt.txt') and os.path.isfile(main_path+'/promt.txt'):
#     #         print('File already exists.')
#     # else:
#     #     with open(main_path+'/promt.txt', 'w') as f:
#     #         f.write(record['prompt'])



        
    

    
    
