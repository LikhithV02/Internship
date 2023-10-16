import vertexai
from vertexai.language_models import TextGenerationModel
from examples import (
    chap_1_content,
    chap_1_summary,
    chap_2_content,
    chap_2_summary,
    chap_3_content,
    chap_3_summary
)
import gradio as gr
import PyPDF2
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def get_prompt(chap_1_content,chap_1_summary,chap_2_content,chap_2_summary,chap_3_content,chap_3_summary, text):
    prompt=f"""input: {chap_1_content}

output: {chap_1_summary}

input: {chap_2_content}

output: {chap_2_summary}

input: {chap_3_content}

output: {chap_3_summary}

input: Write a brief summary for this class 10 English chapter.
Chapter content:
{text}

output:
"""
    return prompt

def generate_output(class_name, subject, chapter):
    pdf_file_path = f'''D:\\Projects\\Shivum Internship\\Study_material_generation\\Main_content\\Books\\{class_name}\\{subject}\\{chapter}.pdf'''
    text = extract_text_from_pdf(pdf_file_path)
    # print(text)
    vertexai.init(project="my-demo-401714", location="us-central1")
    parameters = {
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        get_prompt(chap_1_content,chap_1_summary,chap_2_content,chap_2_summary,chap_3_content,chap_3_summary, text),
        **parameters
    )
    # print(get_prompt)
    return response.text


# Define Gradio input and output components
input_components = [
    gr.Dropdown(["Class 10"],
                       label="Select Class"),
    gr.Dropdown(["English"], label="Select Subject"),
    gr.Dropdown(
        ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5", "Chapter 6", "Chapter 7", "Chapter 8", "Chapter 9"], label="Select Chapters"),
]

# Create the Gradio interface
iface = gr.Interface(
    fn=generate_output,
    inputs=input_components,
    outputs="text",
    title="Notes Generator",
    description="Generate Notes based on class, subject, and chapter selection.",
)

# Launch the Gradio app
iface.launch(share=True, server_name="0.0.0.0", server_port=8088)