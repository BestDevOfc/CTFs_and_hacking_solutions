import openai

API_KEY = open("OpenAIKey.key", 'r').read()
openai.api_key = API_KEY
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "What is the difference between black and blue?"}
    ]
)
print(response)
