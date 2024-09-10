import os
from openai import OpenAI
import json
# Replace with your actual OpenAI API key
api_key = "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"

# Set up the API key
openai.api_key = api_key

# Function to make a simple API call to test the OpenAI API
def make_chatgpt_request():
    # Create a chat completion request
    client = OpenAI(
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )

    # Print out the response
    print("Response:", chat_completion['choices'][0]['message']['content'])

# Call the function to test the request
make_chatgpt_request()
