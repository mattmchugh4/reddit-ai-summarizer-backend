import openai

# test openai API request

# Set up your API key
api_key = "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"

# Create a client instance with the API key
client = openai.Client(api_key=api_key)


# Function to make a simple API call to test the OpenAI API
def make_chatgpt_request():
    # Create a chat completion request using the new client method
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
        ],
    )

    # Output the assistant's response
    print("Response:", response.choices[0].message.content)


# Call the function to test the request
make_chatgpt_request()
