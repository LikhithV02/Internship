from examples import (chap_1_content, chap_1_summary, chap_2_content)
import vertexai
from vertexai.language_models import TextGenerationModel

def get_prompt(cha_1_content):
    prompt=f"""
input: Write a brief summary for this class 10 English chapter.
Chapter content:
{cha_1_content}

output:
"""
    return prompt

def generate_output():
    vertexai.init(project="my-demo-401714", location="us-central1")
    parameters = {
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison-32k")
    response = model.predict(
        get_prompt(chap_1_content),
        **parameters
    )
    print(response.text)
    return response.text

generate_output()