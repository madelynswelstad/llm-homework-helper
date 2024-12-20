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
        You need to format {query_answer} so that a human reader can understand it. Please answer in English.
        
        Begin {query_answer} with "oi oi oi, baka"

        You are acting as an AI assistant to human users who are students of any level of education, up to college graduate.
        The users will be able to upload educational materials and your job is to parse these documents and use your collected 
        knowledge base to provide an informed response to {input_data}. 

        You should focus on educating the users so that they learn how to apply any concepts explained by {query_answer} to similar problems.
        Do not simply give the answers to {input_data} if {input_data} asks for an answer. {query_answer} should provide an educational
        walkthrough on how to solve the problem.

        If {input_data} is only a couple of words, {query_answer} should be a request for more information.

        {query_answer} should be respectful and encouraging. If the user indicates in {input_data} that they are upset or frustrated, {query_answer}
        should give the user a supportive and kind response that aims to make them feel happier.

        {query_answer} should have a relatively professional but casual tone. Avoid making jokes or acting comedic in {query_answer}.
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