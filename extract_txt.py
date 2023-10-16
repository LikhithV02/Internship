import PyPDF2
import os

# Set the path to the folder containing the PDF files
pdf_folder = r'D:\Projects\Shivum Internship\Study_material_generation\Main_content\Books\Class 10\English'

# Set the path to the folder where you want to store the text files
txt_folder = r'D:\Projects\Shivum Internship\Study_material_generation\Main_content\Txt'

# Create the destination folder if it doesn't exist
if not os.path.exists(txt_folder):
    os.makedirs(txt_folder)

# Loop through all PDF files in the source folder
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, filename)

        # Create a corresponding text file name in the destination folder
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(txt_folder, txt_filename)

        with open(pdf_path, 'rb') as pdf_file, open(txt_path, 'w', encoding='utf-8') as txt_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                txt_file.write(text)

# All PDFs in the source folder have been converted to text files in the destination folder.
