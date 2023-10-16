import os
import csv

# Specify the folder containing text files
folder_path = 'D:\\Projects\\Shivum Internship\\Study_material_generation\\Main_content\\Summaries'

# List all text files in the folder
text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Create a list to store data
data = []

# Loop through the text files and extract filename and content
for file_name in text_files:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
        data.append([file_name, content])

# Specify the file name for the CSV
csv_file_name = 'dataset.csv'

# Write the data to a CSV file
with open(csv_file_name, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Chapters', 'Summary'])  # Header row
    writer.writerows(data)

print(f'Dataset saved to {csv_file_name}')
