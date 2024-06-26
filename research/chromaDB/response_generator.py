import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import string

# Model
model_name = "meta-llama/Llama-2-7b-chat-hf"

# Reading In Prompts

# Embedding Model Name Used (Same as the one Used In ChromaDB)
embed_model = "all-mpnet-base-v2" # Change Embedding Model Here

csv_name = "Context_Prompts_embed_" + embed_model + ".csv"
df = pd.read_csv(csv_name)

# Getting Prompts and Gold Labels
prompts = list(df.iloc[:,0])
labels = list(df.iloc[:,1])

# Loading in ENV Variables
load_dotenv(".env")
ANYSCALE_KEY = os.environ.get("KEY")
OPENAI_URL = os.environ.get("OPENAI_URL")

# OpenAI Agent Through Anyscale Endpoint
client = OpenAI(
    api_key=ANYSCALE_KEY,
    base_url=OPENAI_URL
)

# Adding to prompt
for i in range(len(prompts)):
    prompts[i] = prompts[i] + '\n' + "Provide a one word answer."

# Sending to llama-7b
temp = 1.0
system_prompt = ""

responses = []

for i in range(len(prompts)):
    response = client.chat.completions.create(
        model=model_name,
        temperature=temp,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompts[i]}
        ]
    )

    responses.append(response.choices[0].message.content)

# String Transformation
def remove_spaces_lower_and_punctuations(input_string):
    # Remove spaces
    input_string = input_string.replace(" ", "")

    # Convert to lowercase
    input_string = input_string.lower()

    # Remove punctuations
    input_string = input_string.translate(str.maketrans('', '', string.punctuation))

    return input_string

transformed_responses = []
for i in range(len(responses)):
    transformed_responses.append(remove_spaces_lower_and_punctuations(responses[i]))

# Saving Responses In a CSV
responses_df = pd.DataFrame(prompts, columns=['Prompts_with_Context'])

responses_df['labels'] = labels
responses_df['responses'] = responses

responses_df

response_csv = "Responses_llama-7b_embed_" + embed_model + ".csv"
responses_df.to_csv(response_csv, index=False)

# Transforming Responses to Be In The Same Format As Gold Labels for Comparison
responses_df['responses'] = transformed_responses

# Getting General Accuracy Score
correct_responses = responses_df[responses_df['responses'] == responses_df['labels']]

acc = (correct_responses['responses'].count() / len(responses)) * 100

print(f"Accuracy: {acc} %")