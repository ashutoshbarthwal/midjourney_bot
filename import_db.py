import os
import json
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON
from concurrent.futures import ThreadPoolExecutor

# Assuming a PostgreSQL database is running locally and you have the following details
DB_NAME = "midjourney"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "0.tcp.in.ngrok.io"
DB_PORT = "18369"

# Configure a PostgresSQL database and initialize SQLAlchemy engine, session and base
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Create a model for our image data
class ImageData(Base):
    __tablename__ = 'images'
    id = Column(String, primary_key=True)
    filename = Column(String)
    prompt = Column(String)
    json_data = Column(JSON)
    variations = relationship('ImageVariation', backref='image')

class ImageVariation(Base):
    __tablename__ = 'image_variations'
    id = Column(Integer, primary_key=True)
    image_id = Column(String, ForeignKey('images.id'))
    variant_name = Column(String)
    variant_path = Column(String)

# This will create the table if it doesn't exist
Base.metadata.create_all(engine)

# Assuming image folders are at this location
BASE_DIR = 'midjourneyRecent'

def count_dirs(directory):
    return len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))])


def load_data_to_db(folders_list):
    # start a new session
    session = Session()
    count=0
    total_count = len(folders_list)
    for folder_name in folders_list:
        # Check if image id is already in database
        image_in_db = session.query(ImageData).get(folder_name)
        if image_in_db:
            print("Image with id {id} already exists in database".format(id=folder_name))
            continue

        main_dir = os.path.join(BASE_DIR, folder_name, 'main')
        
        if os.path.exists(main_dir):
                records_file = os.path.join(main_dir, 'record.json')
                if os.path.isfile(records_file):
                    with open(records_file, 'r') as f:
                        json_data = json.load(f)
                else:
                        json_data = {'prompt':''}
                
                # Get any .png file in main directory
                image_file = next((f for f in os.listdir(main_dir) if f.endswith('.png')), None)
                if image_file:
                    image_file = os.path.join(main_dir, image_file)

                    # create a new ImageData object
                    image_data = ImageData(
                        id=folder_name,
                        filename=image_file,
                        prompt=json_data['prompt'],
                        json_data=json_data,
                    )
                    # add it to the session
                    session.add(image_data)
                    count+=1
                    # add image variations
                    for variant in ['upscale', 'v4-upscale']:
                        variant_dir = os.path.join(BASE_DIR, folder_name, variant)
                        if os.path.exists(variant_dir):
                            for variant_file in os.listdir(variant_dir):
                                variant_path = os.path.join(variant_dir, variant_file)
                                image_variant = ImageVariation(
                                    image_id=folder_name,
                                    variant_name=variant,
                                    variant_path=variant_path
                                )
                                session.add(image_variant)

                    
        print("out of {total_count} images, {count} images processed".format(total_count=total_count, count=count))

    # commit the session to the database
    session.commit()

    # close the session
    session.close()

def chunks(lst, n):
    """Yield n number of striped chunks from lst."""
    for i in range(0, n):
        yield lst[i::n]
MAX_THREADS = 20
files = os.listdir(BASE_DIR)
file_chunks = list(chunks(files, MAX_THREADS))
futures = []
# run the function to load data into database
for i, chunk in enumerate(file_chunks):
    print(f'Chunk {i+1}: {len(chunk)}')

    # Create a thread pool with a maximum of MAX_THREADS threads
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Submit each download task to the thread pool
        futures.append(executor.submit(load_data_to_db, chunk))
        
        # Wait for all tasks to complete
        for future in futures:
            future.result()

