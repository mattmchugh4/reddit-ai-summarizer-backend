import logging

import openai

client = openai.Client(api_key="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")
logger = logging.getLogger(__name__)  # Use the logger configured globally


def send_chatgpt_request(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=16384,  # Adjust based on your needs
            temperature=1.0,  # Adjust for creativity
            stream=True,  # Enable streaming
        )

        response_message = response.choices[0].message.content.strip()

        return response_message

    except Exception:
        # Handle exceptions appropriately
        logger.error("OpenAI API error occurred", exc_info=True)
        return ""
