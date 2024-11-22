import os

import praw


def open_reddit_connection():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")
    refresh_token = os.getenv("REDDIT_REFRESH_TOKEN")

    # Ensure all necessary environment variables are set
    if not all([client_id, client_secret, refresh_token]):
        raise EnvironmentError(
            "Missing one or more required Reddit API environment variables."
        )

    # Initialize the Reddit API connection
    praw_connection = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        user_agent=user_agent,
    )
    return praw_connection
