import openai
import praw
import tiktoken
from flask import jsonify
import json


from comment_scraper import scrape_comments
from web_search import perform_search

openai.api_key = "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"


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


def send_request(input_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": input_message}
        ]
    )

    response_message = response.choices[0].message['content'].strip()
    return response_message


def start_query(search_query):
    # search_query = input("Enter your search query: ")
    # search_query = 'reddit best car to buy for money'
    response_object = {}

    # search_results = perform_search(search_query)
    search_results = perform_search('test')

    response_object['search_results'] = search_results

    praw_connection = open_reddit_connection()


    if search_results:
        # comments = scrape_comments(praw_connection, search_results[0][1])
        comments = scrape_comments(
            praw_connection, 'https://www.reddit.com/r/whatcarshouldIbuy/comments/ri1d1e/whats_the_best_bang_for_your_buck_cars_that_are/')
    else:
        comments = []
        print("No search results found.")

    try:
        json.dumps(comments)
    except TypeError as e:
        print("Error:", e)
        print('hit')
    response_object['comments'] = comments

    # enc = tiktoken.get_encoding("cl100k_base")
    # tokens = enc.encode(comments)
    # print('Number of Tokens:', str(len(tokens)))

    # input_message_with_comments = 'Can you answer the following question |' + search + '| using these reddit comments and knowledge you have from other sources' + " " + comments

    # chat_message = send_request('hello')
    # response_object['chat_message'] = chat_message

    return jsonify(response_object)
