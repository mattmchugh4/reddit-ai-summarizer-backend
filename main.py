# main.py
import openai
from comment_scraper import scrape_comments
from web_search import perform_search
import praw
import tiktoken

from flask import Flask, request, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api', methods=['POST'])
def api():
    # Get the request data
    data = request.get_json()

    # Do some processing with the data
    response = process_request(data)

    # Return the response
    return response


def process_request(data):
    # Process the request data here and return a response
    response_data = "Your request was processed successfully!"
    response = Response(response_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(port=5000)


# openai.api_key = "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"

# client_id = '8nfmaT3Zt1kPSw7FLFfbZg'
# client_secret = 'T2E4wjZSi1CfkjMBYTEoThWaghoE_w'
# user_agent = 'python:RedditCommentScraper:v1.0.0 (by /u/SpoonfulOfBlues)'
# refresh_token = '73131276-pKb3q5pYU0EyoMkNrt-M0-IKUA-e1g'
# reddit = praw.Reddit(client_id=client_id,
#                      client_secret=client_secret,
#                      refresh_token=refresh_token,
#                      user_agent=user_agent)



# while True:
#     search_query = input("Enter your search query: ")
#     search_query = 'reddit best car to buy for money'
#     search_results = perform_search(search_query)

#     for result in search_results:
#         print(result)
#         print('------')

#     comments = scrape_comments(reddit, search_results[0][1])
#     # print("\nScraped comments:")
#     print(comments)

#     enc = tiktoken.get_encoding("cl100k_base")
#     tokens = enc.encode(comments)
#     print('Number of Tokens:', str(len(tokens)))



# # print("\nEnter your question for ChatGPT, or type 'exit' or 'quit' to exit the program.")

# # Append the scraped comments to the question
# # input_message_with_comments = 'Can you answer the following question |' + search + '| using these reddit comments and knowledge you have from other sources' + " " + comments
# # print(input_message_with_comments)

# # response_message = send_request(input_message_with_comments)
# # print(f"\nChatGPT API responded: {response_message}\n")


# def send_request(input_message):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": input_message}
#         ]
#     )

#     response_message = response.choices[0].message['content'].strip()
#     return response_message
