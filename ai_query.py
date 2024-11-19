from openai import OpenAI
import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3

load_dotenv()

open_ai_client = OpenAI(api_key = os.getenv())

def process_query(input_data):
    query_answer = retrieve_similar_documents(query_text=input_data, top_k=3)

    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.chat.completion.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    prompt = f"""
        You need to format {query_answer} so that a human reader can understand it. 
        
        Make {query_answer} really rude and begin {query_answer} with "oi oi oi, baka"
    """

    response = get_completion(prompt)

    return response

def speech_to_text():
    """
    Requires installing
        - PocketSphinx (pip install pocketsphinx)
        - pyaudio (pip install pyaudio)
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening to you poopy")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        query = r.recognize_sphinx(audio)
        return query
    except (sr.UnknownValueError, sr.RequestError):
        return "NOOOOO IT FAILED to get the audio"

def text_to_speech(text, filename="aianswer.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename