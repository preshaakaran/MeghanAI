import requests
import random
import time
import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import datetime
import subprocess
import sys
from config import api_key

def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'ZIRA' in voice.id:
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Some Error Occurred.", str(e))
            sys.exit()
            return "Some Error Occurred. Sorry"

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": api_key}

def format_prompt(message, custom_instructions=None):
    prompt = ""
    if custom_instructions:
        prompt += f""
    prompt += f"{message}"
    return prompt

def generate(prompt, temperature=0.9, max_new_tokens=512, top_p=0.9, repetition_penalty=1.0):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2

    top_p = float(top_p)

    generate_kwargs = {
        'temperature': temperature,
        'max_new_tokens': max_new_tokens,
        'top_p': top_p,
        'repetition_penalty': repetition_penalty,
        'do_sample': True,
        'seed': random.randint(0, 10**7),
    }
    custom_instructions = "Hello"
    formatted_prompt = format_prompt(prompt, custom_instructions)
    
    try:
        payload = {
            "inputs": formatted_prompt,
            **generate_kwargs
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("An error occurred.", str(e))
        sys.exit()
        return None

print("Model started")
if __name__ == '__main__':
    print("Hello")
    say("Hello I am Meghan AI")
    say("Hi, How may I help you?")
    while True:
        user_prompt = takeCommand()
        start = time.time()
        generated_text_list = generate(user_prompt)
        end = time.time()
        if generated_text_list:
            generated_text = ' '.join(item.get('generated_text', '') for item in generated_text_list if isinstance(item, dict))
            generated_text = generated_text.replace('\n', '')
            print("Bot:", generated_text)
            print("Time Taken:", end - start)
            say(generated_text)
            
            
