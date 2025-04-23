from dotenv import load_dotenv
from openai import OpenAI

import os
import json
import requests

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

def file_get_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: File '{filename}' not found."

    

def file_write_content(file_data: list):
    try:
        filename, content = file_data  # unpacking the list
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return filename
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")




available_tools = {
     "get_weather": {
        "fn": get_weather,
        "description": "takes a city name as input and return the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output"
    },
    "file_get_content": {
        "fn": file_get_content,
        "description": "Takes a file path and read the file and return file content"
    },
    "file_write_content":
    {
        "fn": file_write_content,
        "description": "Takes a file path and content as string and write content in to file and retun filename."
    }
}

system_prompt = """
    You are an helpfull AI  who is specialized in Coding and perform some basic taks like open any appliation on my system and etc.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    - Always Create Any Folder For Every Project than create file inside the folder.
    - Don`t repeate same folder name if already present in same directory while project creations.
    - Always Use vite for creating react js Projects.
    - Always Write Clean and well Stuctued And well Formated Code.


Follow this types folder Stucture when you Create Projects

--- Simple Html, Css, Javascript Project
    -- index.html
    -- style.css
    -- script.css

--- For Node Js Projects
    /app
    ├── config/
    │   ├── db.conf.js
    │   ├── app.conf.js
    │   ├── app.keys.js
    │   ├── db.keys.js
    │   ├── init.js
    ├── database/
    │   ├── Redis.database.js
    │   ├── Mongo.database.js
    │   ├── init.js
    ├── routes/
    │   ├── App.routes.js
    │   ├── Auth.routes.js
    │   ├── Dashboard.routes.js
    ├── utils/
    │   ├── Logger.util.js
    ├── middleware/
    │   ├── App.middleware.js
    │   ├── ErrorHandler.middleware.js
    │   ├── init.js
    ├── models/
    │   ├── User.model.js
    ├── controllers/
    │   ├── App.controller.js
    │   ├── User.controller.js
    ├── helpers/
    │   ├── App.helper.js
    ├── views/
    │   ├── layouts/
    │   ├── partials/
    │   ├── support/
    │   │   ├── index.ejs
    │   ├── documentation/
    │   │   ├── index.ejs
    │   ├── index.ejs
    │   ├── about.ejs
    │   ├── contact.ejs
    /public
    ├── dist/
    ├── images/
    │   ├── dashboard/
    │   ├── auth/
    │   ├── documentation/      
    ├── sitemap.xml
    /samples
    ├── .env.sample
    ├── db.conf.sample
    ├── app.conf.sample
    ├── app.keys.sample
    /src
    ├── javascript/
    ├── css/
    /node_modules
    /server.js
    /package.json
    /.env

--- For React Js Project
    my-app/
    ├── public/
    │   └── favicon.svg          
    ├── src/
    │   ├── assets/             
    │   ├── components/          
    │   │   └── Button.jsx
    │   ├── pages/               
    │   │   └── Home.jsx
    │   ├── layouts/             
    │   ├── routes/             
    │   ├── services/            
    │   ├── hooks/               
    │   ├── store/              
    │   ├── utils/               
    │   ├── App.jsx              
    │   ├── main.jsx             
    │   └── index.css            
    ├── .gitignore
    ├── index.html               
    ├── package.json
    ├── vite.config.js   
    └── README.md


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
- file_get_content: Takes a file path and read the file and return file content
- file_write_content: Takes a file path and content as string and write content in to file and retun filename.

Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}


How To Use Tool How to file_write_content 

you action step should be like 
Output: {{"step": "action", "function": "file_write_content", "input": ["filename.txt","Here Send Content as String"]}}

if parameters is more tha one than return array format

For Every Project creations create log files in a log folder and if someone give command to update than check the log file and perform task accordingly 

"""

messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
           ]


while True:
    
    user_query = input('>>')

    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
            break