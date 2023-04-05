import openai
import os

try:
    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
    print('ENV environment variable exists')
except KeyError:
    print('ENV environment variable does not exist')


messages = [
    {"role": "system", "content": "You are a kind helpful assistant."}
]

while True:
    message = input("User : ")
    if message:
        messages.append(
            {"role": "user", "content": message}
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat.choices[0].message.content
    print(reply)
    messages.append({"role": "system", "content": reply})

