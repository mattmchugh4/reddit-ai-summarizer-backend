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

    chatGPT_question = 'Can you analyze these Reddit comments, and give me a summary of each comment chain? This is a post discussing which car is the best value'\
        'The post is titled "What’s the best bang for your buck cars that are at most 3 years old?" and the original post reads "I’m planning to buy a new car and I’m curious about your thoughts on best bang for your buck cars. It can be any car(cheap or expensive, SUV or sports). The only criteria is it should be at most 3 years old.'\
        'I will input the comments in an 2D array, formatted like so [[Comment, Reply 1, Reply 2, Etc.],[Comment Chain 2], [Chain 3], etc]. Each comment chain is a reply/discussion regarding the original post.'

    filename = "text-input.txt"


# Read the content of the text file into a string variable
    with open(filename, "r") as file:
        file_content = file.read()


# Concatenate the chatGPT_question string with the content of the text file
    chatGPT_message = chatGPT_question + "\n" + file_content

# Pass the resulting string to the send_request function
    chat_message = send_request(chatGPT_message)

    response_object['chat_message'] = chat_message


    summaries = chat_message.split('\n\n')
    response_object['summaries'] = summaries



    return jsonify(response_object)
