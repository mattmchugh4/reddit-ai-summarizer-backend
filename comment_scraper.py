

# import praw
# import tiktoken


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


def format_comment(comment, depth=0):
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

    formatted_comments = []
    for comment in post.comments:
        formatted_comments.append(format_comment(comment))

    print(formatted_comments)
    return formatted_comments



# comments = scrape_comments(
#     reddit, 'https://www.reddit.com/r/whatcarshouldIbuy/comments/ri1d1e/whats_the_best_bang_for_your_buck_cars_that_are/')
# print(comments[0])


# scrape_comments(
#     reddit, 'https://www.reddit.com/r/whatcarshouldIbuy/comments/ri1d1e/whats_the_best_bang_for_your_buck_cars_that_are/')
