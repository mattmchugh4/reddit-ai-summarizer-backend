

# import praw


# client_id = '8nfmaT3Zt1kPSw7FLFfbZg'
# client_secret = 'T2E4wjZSi1CfkjMBYTEoThWaghoE_w'
# user_agent = 'python:RedditCommentScraper:v1.0.0 (by /u/SpoonfulOfBlues)'
# refresh_token = '73131276-pKb3q5pYU0EyoMkNrt-M0-IKUA-e1g'
# reddit = praw.Reddit(client_id=client_id,
#                      client_secret=client_secret,
#                      refresh_token=refresh_token,
#                      user_agent=user_agent)


# function that prints all comments in easy to read format
# def print_comment(comment, depth=0):
#     print("  " * depth, comment.body)
#     print("  " * depth, comment.score)
#     print("  " * depth, "_____________________________________________________________________________________________________________________")
#     print()

#     for reply in comment.replies:
#         print_comment(reply, depth + 1)


# def scrape_comments(reddit, post_url):
#     post_id = post_url.split('/')[-3]
#     post = reddit.submission(id=post_id)

#     # Replace "more_comments" with actual comments
#     post.comments.replace_more(limit=None)

#     for comment in post.comments:
#         print_comment(comment)
#         print("======================================== Comment Chain End ========================================")
#         print()

#     return post.comments
from datetime import datetime

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")


def format_comment(comment, depth=0):

    if comment.author is None or comment.body in ["[deleted]", "[removed]"]:
        return []

    if depth > 5 or comment.score <= -3:
        return []

    if depth == 0:
        formatted_comment = [f"COMMENT ({comment.score}): {comment.body}"]
    else:
        formatted_comment = [
            f"REPLY {depth} ({comment.score}): {comment.body}"]

    if depth < 5:
        for reply in comment.replies:
            formatted_comment.extend(format_comment(reply, depth + 1))

    return formatted_comment


def scrape_comments(reddit, post_url):
    post_id = post_url.split('/')[-3]
    post = reddit.submission(id=post_id)

    # Replace "more_comments" with actual comments
    post.comments.replace_more(limit=None)

    comments = {}
    formatted_comments = []
    comment_string_split = []
    comment_string = ''
    tokens = 0

    for comment in post.comments:
        comment_string += '__break__\n'
        new_comment_chain = format_comment(comment)
        formatted_comments.append(new_comment_chain)

        for new_comment in new_comment_chain:
            comment_string += new_comment + ' '
            # tokens += len(enc.encode(new_comment))

        tokens = len(enc.encode(comment_string))
        if tokens > 2000:
            comment_string_split.append(comment_string)
            comment_string = ''

        comment_string += '\n'

    comment_string_split.append(comment_string)

    comments['title'] = post.title
    comments['initial_post'] = post.selftext

    post_date = post.created_utc

    post_date_formatted = datetime.utcfromtimestamp(
        post_date).strftime('%m/%d/%Y')

    comments['post_date'] = post_date_formatted

    comments['formatted_comments'] = formatted_comments
    comments['comment_strings'] = comment_string_split

    return comments


# comments = scrape_comments(
#     reddit, 'https://www.reddit.com/r/whatcarshouldIbuy/comments/ri1d1e/whats_the_best_bang_for_your_buck_cars_that_are/')
