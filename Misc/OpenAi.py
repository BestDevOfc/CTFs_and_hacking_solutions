import requests
import openai

API_KEY = open("OpenAIKey.key", 'r').read()
openai.api_key = API_KEY

def query_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    return response

def get_user_info():
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    req = requests.get(url="https://api.openai.com/v1/me", headers=headers)
    print(f"[ User Info ]: {req.text}")
    with open("UserInfo.json", 'wb') as f:
        f.write(req.content)

prompt = "What is the difference between black and blue?"
response = query_ai(prompt)
print(response)

get_user_info()
