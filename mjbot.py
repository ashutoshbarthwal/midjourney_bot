import os
import re
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 100

def check_file_exists_else_create(file_path,filename,data=None,mode='w',url=None,ignoreCheck=False):
    if not ignoreCheck and os.path.exists(file_path+'/'+filename) and os.path.isfile(file_path+'/'+filename):
        print('File already exists.')
    else:
        if url:
            response = requests.get(url)
            data = response.content
        with open(file_path+'/'+filename, mode) as f:
            f.write(data)
        print(f'Downloaded variable {file_path} and saved as {filename}')

def processRecord(record):
    print("Processing record: "+record['id'])
    main_path = directory+'/'+record['id']+'/main'
    os.makedirs(main_path, exist_ok=True)
    for image_url in record['image_paths']:
        image_name = image_url.split('/')
        check_file_exists_else_create(main_path,image_name[-1],url=image_url,mode='wb')
    
    variations = directory+'/'+record['id']+'/'+record['event']['eventType']
    os.makedirs(variations, exist_ok=True)
    image_path = record['event']["seedImageURL"]

    for i in range(4):
        var_image_name = '0_'+str(i)+'.png'
        var_image_path = re.sub(r'0_[0-9].png',var_image_name , image_path)
        check_file_exists_else_create(variations,var_image_name,url=var_image_path,mode='wb')
    
    check_file_exists_else_create(main_path,'promt.txt',record['prompt'])
    check_file_exists_else_create(main_path,'record.json',json.dumps(record))

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
data_str = now.strftime('%Y%m%d%')
data_time_str = now.strftime('%Y%m%d%H%M')
directory = 'midjourneyRecent'

print(data_time_str)

# Create the save directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Specify output file name
filename_main= 'response - '+data_time_str+'.json'

check_file_exists_else_create(directory,filename_main,json_string)

# Access the desired data from the JSON object
data = json_object['props']['pageProps']['jobs']


# Create a thread pool with a maximum of MAX_THREADS threads
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    # Submit each download task to the thread pool
    futures = [executor.submit(processRecord, record) for record in data]
    
    # Wait for all tasks to complete
    for future in futures:
        future.result()



        
    

    
    
