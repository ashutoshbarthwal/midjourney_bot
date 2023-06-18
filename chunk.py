import os

directory = 'midjourneyRecent'
files = os.listdir(directory)
num_chunks = 5  # replace with the number of chunks you want

def chunks(lst, n):
    """Yield n number of striped chunks from lst."""
    for i in range(0, n):
        yield lst[i::n]

file_chunks = list(chunks(files, num_chunks))

for i, chunk in enumerate(file_chunks):
    print(f'Chunk {i+1}: {len(chunk)}')