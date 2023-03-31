# comment_scraper.py
import praw


def scrape_comments(post_url):
    client_id = '8nfmaT3Zt1kPSw7FLFfbZg'
    client_secret = 'T2E4wjZSi1CfkjMBYTEoThWaghoE_w'
    user_agent = 'python:RedditCommentScraper:v1.0.0 (by /u/SpoonfulOfBlues)'
    refresh_token = '73131276-pKb3q5pYU0EyoMkNrt-M0-IKUA-e1g'

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         refresh_token=refresh_token,
                         user_agent=user_agent)

    # Extract the post ID from the URL
    post_id = post_url.split('/')[-3]

    # Get the post by ID
    post = reddit.submission(id=post_id)

    # Replace "more_comments" with actual comments
    post.comments.replace_more(limit=None)

    comments_text = ""
    for comment in post.comments:
        comments_text += f"({comment.score}p): {comment.body}\n"
        for reply in comment.replies:
            comments_text += f"({reply.score}p): {reply.body}\n"


    comments_text = comments_text[:12000]

    return comments_text
