import os
from dotenv import load_dotenv

load_dotenv()

from google import genai


API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key = API_KEY)

def call_generate_text(prompt: str):
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )

    print(response)
    return response.text