# test_grok_code_fast.py

from dotenv import load_dotenv
import os
from xai_sdk import Client
from xai_sdk.chat import user, system

# Load environment variables from .env.local file
load_dotenv(".env.local")

# Get the API key (it will now be available because we loaded the file)
api_key = os.getenv("XAI_API_KEY")

if not api_key:
    raise ValueError("XAI_API_KEY not found! Make sure .env.local exists and contains XAI_API_KEY=your_key")

# Create the xAI client
client = Client(api_key=api_key)

# Start a new chat with the grok-code-fast-1 model
chat = client.chat.create(model="grok-code-fast-1")

# Optional: Add a system message to set the behavior
chat.append(system("You are an expert coding assistant that explains your reasoning step by step."))

# Add your user message (change this to whatever you want!)
chat.append(user("Write a Python function that reverses a string without using built-in reverse methods or slicing with [::-1]. Include comments and test it with 'hello' and 'racecar'."))

# Get the response from the model
response = chat.sample()

# Print the model's reply
print("\nGrok Code Fast Response:\n")
print(response.content)
