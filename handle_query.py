import openai
import praw
from flask import jsonify
import json
import asyncio
import httpx


from comment_scraper import scrape_comments
from web_search import perform_search

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

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
    response_object = {}

    # search_results = perform_search(search_query)
    # response_object['search_results'] = search_results

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

    chatGPT_summaries = []

    chatGPT_question = 'Can you concisely summarize the main points for the Reddit comment chain that is pasted below?' \
        f'This comment chain is in response to a post ,  Title: {comments["title"]}; Body: {comments["initial_post"]}.'

    index = 0
    for comment_chain in comments['formatted_comments']:
        if index > 20:
            break
        print(index)
        index += 1
        joined_comments = "\n".join(comment_chain)

        prompt = chatGPT_question + "\n" + joined_comments
        if len(enc.encode(prompt)) > 3500:
            print('too long')
            continue
        response_object['tokens'] += len(enc.encode(prompt))

        summary = send_request(prompt)
        response_object['tokens'] += len(enc.encode(summary))

        chatGPT_summaries.append(summary)

    all_summaries = "\n".join(chatGPT_summaries)

    print('Overall Summary...')

    chatGPT_question_overall_summary = (
        "Can you analyze these summaries of Reddit post comment chains and provide me an overall summary of the post?" + "\n" + all_summaries
    )
    response_object['tokens'] += len(
        enc.encode(chatGPT_question_overall_summary))

    overall_summary = send_request(chatGPT_question_overall_summary)
    response_object['tokens'] += len(
        enc.encode(overall_summary))

    response_object["summaries"] = chatGPT_summaries
    response_object["overall_summary"] = overall_summary

    return jsonify(response_object)


# async def start_query_async(search_query):
#     response_object = {}

#     # search_results = perform_search(search_query)
#     # response_object['search_results'] = search_results

#     praw_connection = open_reddit_connection()

#     comments = scrape_comments(
#         praw_connection, search_query)

#     response_object['formatted_comments'] = comments['formatted_comments']
#     response_object['post_title'] = comments['title']
#     response_object['post_title'] = comments["initial_post"]

#     chatGPT_summaries = []
#     chatGPT_question = 'Can you summarize the main points in this Reddit comment chain: '
#     index = 0

#     tasks = []

#     for comment_chain in comments['formatted_comments']:
#         if index > 10:
#             break
#         index += 1
#         joined_comments = "\n".join(comment_chain)
#         task = send_request_async(chatGPT_question + "\n" + joined_comments)
#         tasks.append(task)

#     chatGPT_summaries = await asyncio.gather(*tasks)

#     all_summaries = "\n".join(chatGPT_summaries)

#     chatGPT_question_summary = (
#         "I am researching the best way to get a job. Can you analyze these Reddit comment chain summaries and give me the best ?"
#     )

#     new_summary = await send_request_async(chatGPT_question_summary + "\n" + all_summaries)
#     print(new_summary)

#     chatGPT_question_overall_summary = (
#         "Can you analyze these summaries of Reddit post comment chains and provide me an overall summary of the post?"
#     )

#     overall_summary = await send_request_async(
#         chatGPT_question_overall_summary + "\n" + all_summaries
#     )

#     response_object["summaries"] = chatGPT_summaries
#     response_object["overall_summary"] = overall_summary

#     return jsonify(response_object)


# def start_query_sync(search_query):
#     return asyncio.run(start_query_async(search_query))


# async def send_request_async(input_message):
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions",
#             headers={"Authorization": f"Bearer {openai.api_key}"},
#             json={
#                 "model": "gpt-3.5-turbo",
#                 "messages": [{"role": "user", "content": input_message}],
#             },
#         )
#     print(response.json())
#     response_message = response.json(
#     )["choices"][0]["message"]["content"].strip()
#     return response_message
    # chatGPT_question = 'I am going to input processed Reddit comments to you and I would like you to give me a summary for each comment chain. I will input the comment chains in the following format: "COMMENT (score) Text. REPLY 1 (score) Text. REPLY 2 (score) Text. Etc. Each comment chain will be separated by "\n__break__\n". Each comment chain is a reply/discussion regarding the original post. In your output, separate each comment chain summary with two blank lines. Now, please ask me any questions about this input that you don’t understand.'

    # f'The post is titled "{comments["title"]}" and the original post reads "{comments["initial_post"]}"'\
    # 'Do you have any questions?'\

    # chatGPT_message = chatGPT_question + "\n" + comments['comment_strings'][0]

# Pass the resulting string to the send_request function
    # chat_message = send_request(chatGPT_message)
    # print(chatGPT_question)
    # chat_message = send_request(chatGPT_question)
    # print(chat_message)
    # while True:
    #     print()
    #     reply = input()
    #     if reply == 'break':
    #         break
    #     else:
    #         clarify = send_request(reply)
    #         print(clarify)

    # analyzed_comments = send_request(comments['comment_strings'][0])
    # print(analyzed_comments)
