import openai
import praw
import tiktoken

from app.chatGPT_input import format_chatGPT_inputs
from app.comment_scraper import scrape_comments

enc = tiktoken.get_encoding("cl100k_base")


def open_reddit_connection():
    client_id = "8nfmaT3Zt1kPSw7FLFfbZg"
    client_secret = "T2E4wjZSi1CfkjMBYTEoThWaghoE_w"
    user_agent = "python:RedditCommentScraper:v1.0.0 (by /u/SpoonfulOfBlues)"
    refresh_token = "73131276-lpsADDAU_yNVL5kEgMqBm5lzurRUOw"  # Need to refresh this? look at scraper.py
    praw_connection = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        user_agent=user_agent,
    )
    return praw_connection


client = openai.Client(api_key="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")


def send_request(input_message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input_message}],
            max_tokens=1500,  # Adjust based on your needs
            temperature=1.0,  # Adjust for creativity
        )

        response_message = response.choices[0].message.content.strip()

        return response_message
    except Exception as e:
        # Handle exceptions appropriately
        print(f"OpenAI API error: {e}")
        return ""


def start_query(search_query, emit_processed_data, emit_status_message):
    response_object = {}

    praw_connection = open_reddit_connection()

    emit_status_message("Scraping comments...")

    comments = scrape_comments(praw_connection, search_query)

    response_object["formatted_comments"] = comments["formatted_comments"]
    response_object["post_title"] = comments["title"]
    response_object["initial_post"] = comments["initial_post"]
    response_object["post_date"] = comments["post_date"]

    response_object["tokens"] = 0

    emit_status_message("Summarizing Comment Chains...")

    # chatGPT_summaries = format_chatGPT_inputs(comments["formatted_comments"]) # makes async requests which doesn't work with the current setup

    # added below code to replace the async function
    chatGPT_summaries = comments["formatted_comments"]
    # Flatten the list of lists into a single list and convert all items to strings
    flattened_summaries = []
    for summary in chatGPT_summaries:
        if isinstance(summary, list):
            flattened_summaries.extend(summary)  # Add items from nested lists
        else:
            flattened_summaries.append(summary)  # Add string directly

    # Now join the flattened list into a single string
    all_summaries = "\n".join(map(str, flattened_summaries))

    # end of added code
    emit_status_message("Generating Overall Summary...")

    chatGPT_question_overall_summary = (
        "Can you analyze these summaries of Reddit post comment chains and provide me an overall summary of the post?"
        + "\n"
        + all_summaries
    )
    response_object["tokens"] += len(enc.encode(chatGPT_question_overall_summary))

    overall_summary = send_request(chatGPT_question_overall_summary)
    response_object["tokens"] += len(enc.encode(overall_summary))

    response_object["summaries"] = chatGPT_summaries
    response_object["overall_summary"] = overall_summary

    emit_processed_data(response_object)
