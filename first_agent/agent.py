import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI

import os
import json
import requests


engine = pyttsx3.init()
def speak(text):
    print(f"🗣️ Speaking: {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ""


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."

def run_command(command):
    result = os.system(command)
    return result

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "takes a city name as input and return the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output"
    }
}



system_prompt = """
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

Rules:
- follow the output JSON formate
- allways perform one step at a time and wait for the next input
- carefully analized the query

About My Operating system 
I am using windowns 11 it will help you to run commands accordingly my instatuctions.


ABout My self. I am Indal Singh a 24 years old guy who are a software developer who created you.

if i want to create node js project than user javascript with express. 

 Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

Available Tools:
- get_weather: Takes a city name as an input and returns the current weather for the city
- run_command: Takes a command as input to execute on system and returns ouput

Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

"""

messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
           ]

# Voice input
user_query = listen()
if not user_query:
    speak("Sorry, I didn't catch that.")
    exit()

messages.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_output = json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

    if parsed_output.get("step") == "plan":
        print(f"🧠: {parsed_output.get('content')}")
        continue

    if parsed_output.get("step") == "action":
        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")
        if tool_name in available_tools:
            output = available_tools[tool_name]["fn"](tool_input)
            messages.append({
                "role": "assistant",
                "content": json.dumps({"step": "observe", "output": output})
            })
        continue

    if parsed_output.get("step") == "output":
        print(f"🤖: {parsed_output.get('content')}")
        speak(parsed_output.get("content"))
        break