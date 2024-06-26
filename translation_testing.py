from dotenv import load_dotenv
import os
import random
import pandas as pd
import numpy as np
import csv

import google.generativeai as genai


# THIRD PARTY
import openai

# LOCAL
# from dummy_data.db_helpers import add_user, add_reading_record, get_10_reading_records
from chroma.get_embeddings  import query_collection

# model

temp = 1.0

# Loading in ENV Variables
load_dotenv(".env")
ANYSCALE_KEY = os.environ.get("KEY")
OPENAI_URL = os.environ.get("OPENAI_URL")

# OpenAI Agent Through Anyscale Endpoint
client = openai.OpenAI(
    api_key=ANYSCALE_KEY,
    base_url=OPENAI_URL
)





def translated_response():
    
    MODELS = [
        "meta-llama/Llama-2-7b-chat-hf",
        "meta-llama/Llama-2-13b-chat-hf",
        "meta-llama/Llama-2-70b-chat-hf",
        "mistralai/Mistral-7B-Instruct-v0.1",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mistralai/Mixtral-8x22B-Instruct-v0.1",
        "HuggingFaceH4/zephyr-7b-beta",
        "google/gemma-7b-it"
    ]

    model_name = "google/gemma-7b-it"
    # Simulate User Prompt From Dummy Questions for now
    dummy_questions = [
        'What is my plant health?',
        'Should I water my plant?',
        'Which crop should I grow?',
        'Is my crop healthy?',
        'Which crop am I growing?',
        'What is my plant health?',
        'Which crop should I grow?',
        'Is my crop healthy?'
    ]

    # Choosing a Dummy User Prompt At Random
    user_prompt = random.choice(dummy_questions)
    
    # History DB IOT Context
    # records = get_10_reading_records()

    # Extracting First 7 Columns as Rows of Context Store Data
    df = pd.read_csv("crop_recommendation_modified.csv")

    first_seven_columns = df.iloc[:, :]

    # Extracting
    first_seven_columns = np.array(first_seven_columns)

    # String Conversion of Soil Measures
    concatenated_strings = [','.join(map(str, sublist)) for sublist in first_seven_columns]

    # Labelling Data
    labels = ['Nitrogen Content', 'Phosphorous Content', 'Potassium Content',
            'Temperature', 'Humidity', 'pH', 'Rainfall']

    labeled_data = []
    for row in concatenated_strings:
      values = row.split(',')
      transformed_data = ', '.join(f'{label}: {value}' for label, value in zip(labels, values))
      labeled_data.append(transformed_data)
    
    #print(labeled_data)

    records = random.sample(labeled_data, 10)
    #print(records)
    
    #print(str(records))

    # Chroma DB Context (Using Top 2 Matches)
    local_context = query_collection(user_prompt)

    data = []
    for docs in local_context['documents']:
        for doc in docs:
            data.append(doc)
    
    context = ""
    for doc in data:
        context = context + doc + ", " 
    
    # Getting Response
    completion_response = client.chat.completions.create(
        model= model_name,
        temperature= temp,
        messages= [
            {"role": "system", "content": f"You are a helpful assistant who has great knowledge of agriculture. You answer in simple language with no markdown. Keep your answers short, to the point and to a maximum of two sentences. Do not mention technical details in your answer. The user's farmland has the following record: {str(records)} and the following is additional information: {context}"},
            {"role": "user", "content": f"{user_prompt}"}
        ]
    )

    response = completion_response.choices[0].message.content



    # # GEMINI MODEL
    # model_name = "text-davinci-003"

    # # GOOGLE GEMINI
    # genai.configure(api_key="AIzaSyA28f_FsYqTWjC6LlEJbNql1qKF3ojhZ20")
    # model = genai.GenerativeModel('gemini-pro')

    # response = model.generate_content("You have great knowledge of farming.")

    # prompt = f"Give a one sentence answer which is straight to the point. A user's farmland has the following record: {records}. Use this and your own knowledge to answer: , \n {user_prompt}"
    # print(prompt)
    # print()
    # response = model.generate_content(prompt)
 
    # response = response.text


    users_language = "urdu"

    # Translating Response To Local Language of User (Pulled From DB)
    translated_response = client.chat.completions.create(
        model = model_name,
        temperature= temp,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant who has great knowledge of languages. You translate english to local languages for farmers in Pakistan."},
            {"role": "user", "content": f"Translate the following into {users_language}: {response}"}
        ]
    )

    translated_response = translated_response.choices[0].message.content


    return user_prompt, response, translated_response

    # return user_prompt, response, translate_response


def save_responses_to_csv(filename, num_responses=10):
    headers = ["user_prompt", "original_response", "translated_response"]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for _ in range(num_responses):
            user_prompt, original, translated = translated_response()
            print()
            print(f"Original Response: {original}")
            print()
            print(f"Translated Response: {translated}")
            print()
            writer.writerow({'user_prompt': user_prompt, 'original_response': original, 'translated_response': translated})

# Example usage:
save_responses_to_csv("responses.csv", num_responses=1)

    

    
