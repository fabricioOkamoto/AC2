import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

response = openai.ChatCompletion.create(
  model="gpt-3.5",
  messages=[],
  temperature=0,
  max_tokens=1024
)