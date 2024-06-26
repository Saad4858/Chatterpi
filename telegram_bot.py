from dotenv import load_dotenv
import os
import time

# THIRD PARTY
import openai
import schedule
import telebot

# LOCAL
from dummy_data.db_helpers import add_user, add_reading_record, get_10_reading_records
from chroma.get_embeddings  import query_collection
from research.chromaDB.weather_api import get_current_weather_data , get_forecast

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

API_KEY = os.getenv("OPENAI_API_KEY")
    
OPENAI_CLIENT = openai.OpenAI(
    api_key=API_KEY,
)

user_chat_id = None
user_pref_language = "urdu"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    global user_chat_id
    user_chat_id = message.chat.id
    bot.reply_to(message, "Welcome to ChatterPi, your personal agriculture assistant! 🌱🤖\nThe current language is set to Urdu. If you would like to change the default language setting, send message 'language:<your preferred language>'.\neg. language:english")

def send_alert():
    global user_chat_id
    if user_chat_id:
        bot.send_message(user_chat_id, "Fetching the latest updates for your farmland... 🌱🌧️")
        
        try:
            records = get_10_reading_records()

            completion_response = OPENAI_CLIENT.chat.completions.create(
                model = 'gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant who has great knowledge of agriculture. You answer in simple language with no markdown. The user's farmland has the following records: {str(records)}"},
                    {"role": "user", "content": f"Please tell me if there's any problem with my farmland and what I can do about it."}
                ]
            )

            bot.send_message(user_chat_id, translate_response(completion_response.choices[0].message.content))
            

        except Exception as e:
            return "Unable to give an update at the moment. I will try again in a bit."

def translate_response(response):
    
    try:

        # Translating Response To Local Language of User (Pulled From DB)
        translated_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of languages. You translate english to local languages for farmers in Pakistan."},
                {"role": "user", "content": f"Translate the following into {user_pref_language}: {response}"}
            ]
        )
        
        return translated_response.choices[0].message.content
    
    except Exception as e:
        
        return "Unable to translate to " + user_pref_language + " at this time. Here's a response in English: " + response

@bot.message_handler(commands=['health'])
def get_crop_health(message):
    send_alert()
    
@bot.message_handler(commands=['improvement'])
def improve_growth(message):
    try:
        records = get_10_reading_records()

        completion_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of agriculture. You answer in simple language with no markdown. The user's farmland has the following records: {str(records)}"},
                {"role": "user", "content": f"Please tell me if there's any problem with my farmland and what I can do about it."}
            ]
        )

        bot.reply_to(message, translate_response(completion_response.choices[0].message.content))

    except Exception as e:
        bot.reply_to(message, "Unable to suggest an improvement at the moment. Please try again later.")
    
@bot.message_handler(commands=['grow'])
def recommend_crop(message):
    try:
        records = get_10_reading_records()

        completion_response = OPENAI_CLIENT.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": f"You are a helpful assistant who has great knowledge of agriculture. You answer in simple language with no markdown. The user's farmland has the following records: {str(records)}"},
                {"role": "user", "content": f"Please recommend a crop and why it is suggested."}
            ]
        )

        bot.reply_to(message, translate_response(completion_response.choices[0].message.content))
    
    except Exception as e:
        bot.reply_to(message, "Unable to recommend a crop at the moment. Please try again later.")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    # Check if the user wants to change the language
    if "language:" in message.text:
        global user_pref_language
        user_pref_language = message.text.split(":")[1]
        bot.reply_to(message, f"Language has been set to {user_pref_language}.")
    else:
        # bot.reply_to(message, "Invalid command. Please use /health, /improvement, /grow or language:<your preferred language>.")
        try:
            records = get_10_reading_records()
            
            # Chroma DB Context (Using Top 2 Matches)
            local_context = query_collection(message.text)

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
                    {"role": "user", "content": f"{message.text}"}
                ]
            )

            response = completion_response.choices[0].message.content

            bot.reply_to(message, translate_response(response))
        
        except Exception as e:
            bot.reply_to(message, "Unable to give a response at this time. Please try again later.")
    
# Schedule the send_alert function to run every 10 minutes
schedule.every(10).minutes.do(send_alert)

# Start the bot polling and keep the scheduler running in the same process
def run_bot():
    print('STARTING TELEGRAM BOT...')
    while True:
        bot.polling(none_stop=True)
        schedule.run_pending()
        time.sleep(1)

run_bot()
