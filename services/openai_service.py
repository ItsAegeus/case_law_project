import openai
from config import OPENAI_API_KEY

def refine_query(user_input: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a legal assistant. Convert user input into a legal search query."},
            {"role": "user", "content": user_input}
        ],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"]