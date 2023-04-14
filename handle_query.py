import openai
import praw
from flask import jsonify
import asyncio
import httpx

from chatGPT_input import format_chatGPT_inputs
from comment_scraper import scrape_comments

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

def open_reddit_connection():
    client_id = '8nfmaT3Zt1kPSw7FLFfbZg'
    client_secret = 'T2E4wjZSi1CfkjMBYTEoThWaghoE_w'
    user_agent = 'python:RedditCommentScraper:v1.0.0 (by /u/SpoonfulOfBlues)'
    refresh_token = '73131276-pKb3q5pYU0EyoMkNrt-M0-IKUA-e1g'
    praw_connection = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  refresh_token=refresh_token,
                                  user_agent=user_agent)
    return praw_connection


# openai.api_key = "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"

def send_request(input_message):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": input_message}
            ]
        )

        response_message = response.choices[0].message['content'].strip()
        return response_message


def start_query(search_query, emit_processed_data):
    response_object = {}

    praw_connection = open_reddit_connection()
    print('Scraping comments...')

    comments = scrape_comments(
        praw_connection, search_query)

    response_object['formatted_comments'] = comments['formatted_comments']
    response_object['post_title'] = comments['title']
    response_object['initial_post'] = comments["initial_post"]
    response_object['post_date'] = comments["post_date"]

    response_object['tokens'] = 0

    print('Summarizing Chains...')

    format_chatGPT_inputs(comments['formatted_comments'])


    # all_summaries = "\n".join(chatGPT_summaries)

    # print('Overall Summary...')

    # chatGPT_question_overall_summary = (
    #     "Can you analyze these summaries of Reddit post comment chains and provide me an overall summary of the post?" + "\n" + all_summaries
    # )
    # response_object['tokens'] += len(
    #     enc.encode(chatGPT_question_overall_summary))

    # overall_summary = send_request(chatGPT_question_overall_summary)
    # response_object['tokens'] += len(
    #     enc.encode(overall_summary))

    # response_object["summaries"] = chatGPT_summaries
    # response_object["overall_summary"] = overall_summary

    # emit_processed_data(response_object)
