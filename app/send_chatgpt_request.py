import logging
import os

import openai

logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set in the environment")

client = openai.Client(api_key=api_key)


def send_chatgpt_request(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=16384,
            temperature=1.0,
            # stream=True,
        )

        response_message = response.choices[0].message.content.strip()

        return response_message

    except Exception:
        # Handle exceptions appropriately
        logger.error("OpenAI API error occurred", exc_info=True)
        return ""


def flatten_summaries(summaries):
    """
    Flatten a list of summaries, ensuring all elements are strings and concatenated with newlines.
    """
    flattened = []
    for summary in summaries:
        if isinstance(summary, list):
            flattened.extend(map(str, summary))
        else:
            flattened.append(str(summary))
    return "\n".join(flattened)


def construct_messages(comments, all_summaries, user_question):
    """
    Construct the messages payload for the GPT request.
    """
    system_message = "You are an AI assistant that provides helpful answers based on Reddit discussions."

    user_message = (
        f"**Reddit Post Title:**\n{comments['title']}\n\n"
        f"**Reddit Post Content:**\n{comments['initial_post']}\n\n"
        f"**Summarized Comments:**\n{all_summaries}\n\n"
        "Based on this Reddit discussion, please answer the following question:\n\n"
        f"**User Question:**\n{user_question}\n\n"
        "Your answer should summarize the relevant information from the Reddit data and provide additional context or insights as needed. Use markdown formatting to structure your response."
    )

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
