import tiktoken

from app.comment_scraper import scrape_comments
from app.open_reddit_connection import open_reddit_connection
from app.send_chatgpt_request import send_chatgpt_request

# from app.chatGPT_input import format_chatGPT_inputs


enc = tiktoken.get_encoding("cl100k_base")


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

    overall_summary = send_chatgpt_request(chatGPT_question_overall_summary)
    response_object["tokens"] += len(enc.encode(overall_summary))

    response_object["summaries"] = chatGPT_summaries
    response_object["overall_summary"] = overall_summary

    emit_processed_data(response_object)
