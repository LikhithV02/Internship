import vertexai
from vertexai.language_models import TextGenerationModel
from google.cloud import aiplatform
from google.auth import exceptions
import Key_points
import gradio as gr
import PyPDF2
import sumerize
import os
from pdfminer.high_level import extract_text
# Authenticate using the API key
# Set the API key as an environment variable

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Projects\Shivum Internship\Study_material_generation\Main_content\key.json"

vertexai.init(project="study-material-generator", location="us-central1")


def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


def get_prompt(text, subject, topic):
    prompt = f"""
	  you are given a {subject} topic
	  {text}
	  Create the well Structured detailed Notes as a html code in the following template. Consider the following points while creating the template.
	  1. Introduction part must have minimum 500 words
	  2. In the notes part please describe each topic in detail with word count 1000
	  3. Key points part must have minimum 250 words.
	  4. The notes should be on topic.
	<!DOCTYPE html>
	<html>
	<head>
	    <meta charset="UTF-8">
	    <title>Chapter Study Material </title>
	</head>
	<body>
	    <h1>Study Material</h1>
	    <h3>1. Introduction</h3>
	    <p>
		<!-- Replace with your introduction content-->
	    </p>

	    <h3>2.Important Topics in detail from the chapter. </h3>
		<!--Describe the important topics don't forget the equations, formulas and other things replated to the topic.Describe and elaborate each of the topic and formula and equation-->
	  	<h4><!-- Heading of topic 1>r</h4>
	  	<p>
	  	   <!--Describe the topic in 100 words and bullet out the subtopic and describe if any-->
	  	   <!-- Equations and formulas if any-->
	  	</P>
	  	 <h4><!-- Heading of topic 2>r</h4>
	  	<p>
	  	   <!--Describe the topics in 100 words bullet out the subtopic and describe if any-->
	  	   <!-- Equations and formulas if any-->
	  	</P>
	  	<h4><!-- Heading of topic 3>r</h4>
	  	<p>
	  	   <!--Describe the topics in 100 words bullet out the subtopic and describe if any-->
	  	   <!-- Equations and formulas if any-->
	  	</P>
	  	<!-- Like wise add all possible topics from the chapter-->
	     <h3> Key Points from the chapter </h3>
	     <p> <!--Replace with your key points content in bullet points-->
	</body>
	</html>

	  """
    prompt2 = f"""
  	Create detailed study material from the given Chapter from a book by considering the following points in mind
		1.Ensure a thorough understanding of the chapter's main ideas and themes.
		2.Identify and emphasise essential concepts and arguments.
		3.Create a well-organised outline reflecting the chapter's structure.
		4.Provide concise, to-the-point summaries for each section.
		5.Define and clarify key terms and concepts introduced in the chapter.
		6.Pose engaging questions for self-assessment and discussion.
		7.Ensure accurate citations for quotes and references.
		8.use given text only for reference you can add as much as detail you can.
		9.The response should be complete.
		10.Generate response as a html page with all type of formatting.
		11.Each point you take in the study material please describe it in detail.
	Use the following HTML template to structure your notes:
	<!DOCTYPE html>
	<html>
	<head>
	    <meta charset="UTF-8">
	    <title>Chapter Study Material</title>
	</head>
	<body>
	    <h1>Chapter Study Material</h1>
	    <h3>1. Introduction</h3>
	    <p>
		<!-- Replace with your introduction content -->
	    </p>

	    <h3>2. Describe important Points in detail from the chapter</h3>
	    <h4><!-- Heading of topic 1>r</h4>
	  	<p>
	  	   <!--Describe the topics in detail and elaborate it and bullet out the subtopic and describe if any-->
	  	</P>
	  	 <h4><!-- Heading of topic 2>r</h4>
	  	<p>
	  	   <!--Describe the topics in detail and elaborate bullet out the subtopic and describe if any-->
	  
	  	</P>
	  	<h4><!-- Heading of topic 3>r</h4>
	  	<p>
	  	   <!--Describe the topics 3 in detail and elaborate-->
	  	</P>
			<!-- Like wise add all possible topics from the chapter-->
	    <h3>3. Summary</h3>
	    <p>
		<!-- Replace with your summary content -->
	    </p>

	    <!-- Additional content can be added as needed -->
	</body>
	</html>
	Chapter Context:
	{text}"""

    prompt3 = f"""
  Create detailed study material from the given given topic from a book chapter by considering the following points in mind
	1.Notes will be based on topic specific.
	2.Ensure that explanations are clear and concise, using simple language to make complex concepts understandable.
	3.Highlight key concepts, theories, and important formulas related to each topic in detail.
	4.For  mathematical components like physics and chemistry, provide step-by-step solutions for numerical problems.
	5.The notes should be in detail cover all the concepts related to the topic.
	6.use given text only for reference you can add as much as detail you can.
	7.The response should be  complete.
	8.Ignore unnecessary information in the context.
	9.Generate response as a valid 'html' page with all type of formatting.

	Topic: - {topic}
	Content:- 
	 {text}"""
    return prompt2 if subject == "English" else prompt3


def generate_pdf(class_name, subject, chapter, text, topic):
    pdf_filename = f"{class_name}_{subject}_{chapter}_{topic}.html"
    with open(pdf_filename, "w") as file:
        file.write(text)
    return pdf_filename


def pdf_generator(class_name, subject, chapter, query):
    # Create a list to store the generated PDF file paths
    pdf_paths = []
    if query == "no-input-recieved":
        pdf_file_path = f"D:\\Projects\\Shivum Internship\\Study_material_generation\\Main_content\\Books\\{class_name}/{subject}/{chapter}.pdf"
        pdf_text = sumerize.summarize_text(
            extract_text_from_pdf(pdf_file_path))
        study_material = generate_study_material(pdf_text, subject, query)
        print("study material==", study_material, end='\n')
        pdf_filename = generate_pdf(
            class_name, subject, chapter, study_material, query)
        pdf_paths.append(pdf_filename)
        return pdf_paths
    
    points = query.split(",")
    for point in points:
        pdf_file_path = f"D:\\Projects\\Shivum Internship\\Study_material_generation\\Main_content\\Books\\{class_name}/{subject}/{chapter}.pdf"
        pdf_text = extract_text_from_pdf(pdf_file_path)
        pdf_text = Key_points.retrieve(pdf_file_path, point)
        study_material = generate_study_material(pdf_text, subject, point)
        pdf_filename = generate_pdf(
            class_name, subject, chapter, study_material, point)
        pdf_paths.append(pdf_filename)
    return pdf_paths


def generate_study_material(pdf_text, subject, topic):
    print(get_prompt(pdf_text, subject, topic))
    parameters = {
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        get_prompt(pdf_text, subject, topic),
        **parameters
    )
    return response.text


# Define Gradio input and output components
input_components = [
    gr.inputs.Dropdown(["Class 10", "Class 11", "Class 12"],
                       label="Select Class"),
    gr.inputs.Dropdown(["Math", "Science", "English",
                       "Chemistry"], label="Select Subject"),
    gr.inputs.Dropdown(
        ["Chapter 1", "Chapter 2", "Chapter 3"], label="Select Chapters"),
    gr.inputs.Textbox(
        label="Write the topics name saperated by ','", default="no-input-recieved")
]

output_component = gr.outputs.File(label="Download PDFs")

# Create the Gradio interface
iface = gr.Interface(
    fn=pdf_generator,
    inputs=input_components,
    outputs=output_component,
    title="PDF Generator",
    description="Generate PDFs based on class, subject, and chapter selection.",
)

# Launch the Gradio app
iface.launch(share=True, server_name="0.0.0.0", server_port=8088)
