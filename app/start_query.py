from app.comment_scraper import scrape_comments
from app.open_reddit_connection import open_reddit_connection
from app.send_chatgpt_request import (
    construct_messages,
    flatten_summaries,
    send_chatgpt_request,
)

# enc = tiktoken.get_encoding("cl100k_base")


def start_query(search_query, user_question, emit_processed_data, emit_status_message):
    response_object = {}

    praw_connection = open_reddit_connection()

    emit_status_message("Scraping comments...")
    comments = scrape_comments(praw_connection, search_query)

    # Populate response_object with scraped data
    response_object.update(
        {
            "formatted_comments": comments["formatted_comments"],
            "post_title": comments["title"],
            "initial_post": comments["initial_post"],
            "post_date": comments["post_date"],
        }
    )

    emit_status_message("Summarizing Comment Chains...")
    chatGPT_summaries = comments["formatted_comments"]

    # Flatten the summaries
    all_summaries = flatten_summaries(chatGPT_summaries)

    emit_status_message("Generating Answer...")
    messages = construct_messages(comments, all_summaries, user_question)

    overall_summary = send_chatgpt_request(messages)

    response_object["summaries"] = chatGPT_summaries
    response_object["overall_summary"] = overall_summary

    emit_processed_data(response_object)
    emit_status_message("Response complete")
