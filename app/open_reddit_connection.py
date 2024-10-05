import praw


def open_reddit_connection():
    client_id = "8nfmaT3Zt1kPSw7FLFfbZg"
    client_secret = "T2E4wjZSi1CfkjMBYTEoThWaghoE_w"
    user_agent = "python:RedditCommentScraper:v1.0.0 (by /u/SpoonfulOfBlues)"
    refresh_token = "73131276-lpsADDAU_yNVL5kEgMqBm5lzurRUOw"  # Need to refresh this? look at scraper.py
    praw_connection = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        user_agent=user_agent,
    )
    return praw_connection
