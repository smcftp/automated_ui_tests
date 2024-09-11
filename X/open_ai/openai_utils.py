from openai import OpenAI

import json

from config import settings
from open_ai.tweet_promt import promt

client = OpenAI(
    api_key=settings.openai_api_key
)
   
def generate_tweet() -> str: 
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages = [
                {"role": "system", "content": "You are a content maker for a Star Wars themed Twitter account."},
                {"role": "user", "content": "{}".format(promt)}
            ]
        )
            
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при генерации твита через OpenAI: {e}")
        return "Забавный пост не смог быть сгенерирован!"