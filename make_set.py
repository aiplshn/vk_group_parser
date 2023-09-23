import os

result_folder = 'results'
files = os.listdir(result_folder)
result = set()

for file in files:
    f = open(os.path.join(result_folder, file))
    for line in f:
        result.add(line)

with open(os.path.join(result_folder, 'results.txt'), 'w') as f:
    for url in result:
        if url != '' and url != '\n':
            f.write(url)
