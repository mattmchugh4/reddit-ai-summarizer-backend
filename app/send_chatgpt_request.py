import openai

client = openai.Client(api_key="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")


def send_chatgpt_request(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=100_000,  # Adjust based on your needs
            temperature=1.0,  # Adjust for creativity
        )

        response_message = response.choices[0].message.content.strip()

        return response_message
    except Exception as e:
        # Handle exceptions appropriately
        print(f"OpenAI API error: {e}")
        return ""
