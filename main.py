# STANDARD
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
import threading
import time
import csv
import json
import random

# THIRD PARTY
import openai

# LOCAL
from dummy_data.db_helpers import add_user, add_reading_record, get_10_reading_records
from chroma.get_embeddings  import query_collection
from research.chromaDB.weather_api import get_current_weather_data , get_forecast

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPENAI_API_KEY")

    
OPENAI_CLIENT = openai.OpenAI(
    api_key=API_KEY,
)

def simulate_iot_devices():
    print("Started simulating IoT Devices")
    with open('./dummy_data/crop_recommendation.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print('Adding row')
            row['user_id'] = 1
            add_reading_record(row)
            time.sleep(5)

iot_thread = threading.Thread(target=simulate_iot_devices)
# iot_thread.start()


@app.get("/") 
async def root(request: Request): 
    return {"message":"You Got Hello World!"}

@app.post("/") 
async def root(request: Request): 
    body = await request.json()

    body.update({"message":"You Posted Hello World!"})
    return body

@app.get("/something") 
async def something(request: Request): 
    return {"message":"something"}

@app.get("/bla")
async def bla(request: Request):
    return {"message":"bla"}

@app.post("/bot/")
async def receive_message(request: Request):
    # Read JSON directly from the request body
    json_data = await request.json()
    return json_data


@app.post("/generate-response/")
async def generate_response(metrics: str):

    # load the OPENAI_API_KEY from the environment
    API_KEY = os.getenv("OPENAI_API_KEY")
    
    client = openai.OpenAI(
        api_key=API_KEY,
    )
    
    prompt = f"Given the following agricultural metrics: {metrics}. Which crops should be grown? Give the answer in the form of a list of crops most suitable for the given metrics."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ]
        )
        return response.choices[0].message
    except Exception as e:
        return str(e)
    
@app.post('/makeUser')
async def make_user(request:Request):
    try:
        add_user()
        return {'message':'user added'}
    except Exception as e:
        print(e)
        return {'message':'failure adding user'}
    
@app.get('/latestRecordsMessage')
async def get_latest_records_message(request:Request):
    try:
        records = get_10_reading_records()

        completion_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of agriculture. You answer in simple language with no markdown. The user's farmland has the following records: {str(records)}"},
                {"role": "user", "content": f"Please recommend a crop and why it is suggested. Also tell me if there's any problem with my farmland and what I can do about it."}
            ]
        )

        print(records)
        return {'message':f'{completion_response.choices[0].message.content}'}
    except Exception as e:
        print(e)
        return {'message':'failure getting latest message'}

@app.get('/latestRecordMessage')
async def get_latest_record_message(request:Request):
    try:
        records = get_10_reading_records()

        completion_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of agriculture. You answer in simple language with no markdown. The user's farmland has the following record: {str(records[0])}"},
                {"role": "user", "content": f"Please recommend a crop and why it is suggested. Also tell me if there's any problem with my farmland and what I can do about it."}
            ]
        )

        print(records)
        return {'message':f'{completion_response.choices[0].message.content}'}
    except Exception as e:
        print(e)
        return {'message':'failure getting latest message'}


@app.get('/translatedResponse')
async def get_translated_response(request:Request):
    try:
        # Simulate User Prompt From Dummy Questions for now
        dummy_questions = [
            'What is my plant health?',
            'Should I water my plant?',
            'Which crop should I grow?',
            'Is my crop healthy?',
            'Which crop am I growing?',
            'Which crop has the most profit?',
            'What is my plant health?',
            'Should I water my plant?',
            'Which crop should I grow?',
            'Is my crop healthy?'
        ]

        # Choosing a Dummy User Prompt At Random
        user_prompt = random.choice(dummy_questions)
        
        # History DB IOT Context
        records = get_10_reading_records()

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
        completion_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of agriculture. You answer in simple language with no markdown. Keep your answers short, to the point and to a maximum of two sentences. Do not mention technical details in your answer. The user's farmland has the following record: {str(records)} and the following is additional information: {context}"},
                {"role": "user", "content": f"{user_prompt}"}
            ]
        )

        response = completion_response.choices[0].message.content

        users_language = "urdu"

        # Translating Response To Local Language of User (Pulled From DB)
        translated_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of languages. You translate english to local languages for farmers in Pakistan."},
                {"role": "user", "content": f"Translate the following into {users_language}: {response}"}
            ]
        )

        print(f"You asked: {user_prompt}")
        print(f"Response: {translated_response.choices[0].message.content}")

        return { 'user_prompt': f'{user_prompt}',
                 'original_response': f'{completion_response.choices[0].message.content}',
                 'translated_response': f'{translated_response.choices[0].message.content}',
                 'context' : f'{context}'}
    except Exception as e:
        print(e)
        return {'message':'failure getting latest message'}
    



@app.get('/translatedResponseUser')
async def get_translated_response(request: Request, user_prompt: str , language: str):
    try:
        # History DB IOT Context
        records = ""

        # Chroma DB Context (Using Top 2 Matches)
        local_context = query_collection(user_prompt)

        data = []
        for docs in local_context['documents']:
            for doc in docs:
                data.append(doc)
        
        context = ""
        for doc in data:
            context = context + doc + ", "

        current_weather_data = get_current_weather_data("Lahore")

        forecast , six_hour_forecast = get_forecast("Lahore",3)
        
        context  = context +"\n"+"Considering the weather conditions \n" + current_weather_data
        context = context + "\n" + six_hour_forecast
        # Getting Response
        completion_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of agriculture. You answer in simple language with no markdown. Keep your answers short, to the point and to a maximum of two sentences. Do not mention technical details in your answer. The user's farmland has the following record: {str(records)} and the following is additional information: {context}"},
                {"role": "user", "content": f"{user_prompt}"}
            ]
        )

        response = completion_response.choices[0].message.content

        users_language = language

        # Translating Response To Local Language of User (Pulled From DB)
        translated_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of languages. You translate English to local languages for farmers in Pakistan."},
                {"role": "user", "content": f"Translate the following {response} into {users_language} language."}
            ]
        )

        print(f"You asked: {user_prompt}")
        print(f"Response: {translated_response.choices[0].message.content}")
        

        return { 'user_prompt': f'{user_prompt}',
                 'original_response': f'{response}',
                 'translated_response': f'{translated_response.choices[0].message.content}',
                 'context' : f'{context}',
                 'IOT Rows': f'{records}'
                 }
    
    except Exception as e:
        print(e)
        return {'message':'failure getting latest message'}
