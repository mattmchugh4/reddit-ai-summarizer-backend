
# from bs4 import BeautifulSoup
import praw
import requests

client_id = '8nfmaT3Zt1kPSw7FLFfbZg'
client_secret = 'T2E4wjZSi1CfkjMBYTEoThWaghoE_w'
user_agent = 'python: RedditCommentScraper: v1.0.0 (by / u/SpoonfulOfBlues)'
username = 'SpoonfulOfBlues'
password = 'zIqtus-watbem-jygqa6'
redirect_uri = 'http://localhost:8080'


reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password,
                     redirect_uri=redirect_uri)


auth_url = reddit.auth.url(
    scopes=['identity', 'read'], state='unique_state', duration='permanent')
print("Authorization URL:", auth_url)

# Replace the response_url with the URL containing your code
response_url = 'http://localhost:8080/?state=unique_state&code=3rcy6JrarjXQrMaKJ9K7E86ADgDviQ#_'

code = response_url.split("code=")[1].split("#")[0]
access_token = reddit.auth.authorize(code)
print("Access Token:", access_token)

# Get the refresh token
reddit_user = reddit.user.me()
refresh_token = reddit_user.auth.refresh_token
print("Refresh Token:", refresh_token)

# # Replace the URL with the desired Reddit post URL
# url = 'https://www.reddit.com/r/subreddit/comments/abcdef/post_title/'


# def scrape_comments(url):
#     submission = reddit.submission(url=url)
#     submission.comments.replace_more(limit=None)

#     for comment in submission.comments.list():
#         print(comment.body)


# if __name__ == '__main__':
#     scrape_comments(url)





# # # Replace this URL with the URL of the forum page you want to scrape
# # url = "https://terrylove.com/forums/index.php?threads/should-i-have-re-heated-the-valve.104529/"

# # # Send a request to the forum page
# # response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# # # Parse the HTML content of the page
# # soup = BeautifulSoup(response.content, "html.parser")
# # # text_elements = soup.find_all(text=True)
# # # print(soup)

# # # Filter out unwanted elements like styles, scripts, and document tags
# # # filtered_elements = [element for element in text_elements if element.parent.name not in [
# # #     'style', 'script', 'head', 'title', 'meta', '[document]']]

# # # Print the filtered text elements line by line
# # comment_elements = soup.find_all("div", class_="bbWrapper")

# # # # Iterate through the comment elements and print the text content
# # for comment_element in comment_elements:
# #     comment_text = comment_element.text.strip()
# #     print(f"User comment: {comment_text}\n")
# # # # Find all the comment elements on the page
# # # comment_elements = soup.find_all("div", class_="_1qeIAgB0cPwnLhDF9XSiJM")

# # # # Iterate through the comment elements and print the text content
# # # for comment_element in comment_elements:
# # #     comment_text = comment_element.text.strip()
# # #     print(f"User comment: {comment_text}\n")
