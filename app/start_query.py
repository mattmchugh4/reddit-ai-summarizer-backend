from app.comment_scraper import scrape_comments
from app.open_reddit_connection import open_reddit_connection
from app.send_chatgpt_request import (
    construct_messages,
    flatten_summaries,
    send_chatgpt_request,
)


def start_query(
    search_query,
    user_question,
    emit_processed_data,
    emit_status_message,
    emit_stream,
    emit_post_data,
):
    response_object = {}
    praw_connection = open_reddit_connection()

    emit_status_message("Scraping comments...")
    post = scrape_comments(praw_connection, search_query)

    # Extract post details
    post_data = {
        "post_title": post["title"],
        "initial_post": post["initial_post"],
        "post_date": post["post_date"],
    }

    # Emit post details as a separate event
    emit_post_data(post_data)

    # Continue with processing comments
    response_object.update(
        {
            "formatted_comments": post["formatted_comments"],
            "post_title": post["title"],
            "initial_post": post["initial_post"],
            "post_date": post["post_date"],
        }
    )

    emit_status_message("Summarizing Comment Chains...")
    chatGPT_summaries = post["formatted_comments"]

    # Flatten the summaries
    all_summaries = flatten_summaries(chatGPT_summaries)

    emit_status_message("Generating Answer...")
    messages = construct_messages(post, all_summaries, user_question)

    overall_summary = send_chatgpt_request(messages, emit_stream)

    response_object["summaries"] = chatGPT_summaries
    response_object["overall_summary"] = overall_summary

    emit_processed_data(response_object)
    emit_status_message("Response complete")
