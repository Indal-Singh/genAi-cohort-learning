from openai import OpenAI

import os
import json

client =  OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
You Are A helpfull ai Assistant You Are specialized to Select Best LLM Or Model To Resolved User Query Based On User Query

You have to plan based On the user query after give the output.

Rule: 
- Follow the Output JSON Format.
- Always perform one step at a time and wait for next input
- Carefully analyse the user query

available Models & LLMs
- claude-sonnet-3.7 : This is the Model which is best in coding mainly in frontend part it can also perform backend part as well as.
- gpt-4o : this model is best for perform daily task also best for ppt, excels, word related works and model, it also good for general queryies.
- 

Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "model": "the Model Name which is best to perform User Task.",
    }}


Example:
user Query : Create A Simple Html Website
{{ "step":"plan", "content":"Okay User want To Create a website. it means user query realated To programming and coding" }}
{{ "step":"plan", "content":"I have Select Model realated To Coding." }}
{{ "step":"output", "content":"best model for You query is GPT-4o","model":"gpt-4o"}}
"""

messages = [
    {
        "role":"system",
        "content": system_prompt
    }
]

while True:
    user_query = input(">>")
    messages.append({"role":"user","content":user_query})

    response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

    parsed_output = json.loads(response.choices[0].message.content)
    print(parsed_output)
    messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

    if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            print(f"mdoel: {parsed_output.get('model')}")
            continue