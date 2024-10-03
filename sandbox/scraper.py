import praw
import requests
from requests.auth import HTTPBasicAuth

# Reddit app credentials
client_id = "8nfmaT3Zt1kPSw7FLFfbZg"
client_secret = "T2E4wjZSi1CfkjMBYTEoThWaghoE_w"
user_agent = "python:RedditCommentScraper:v1.0.0 (by /u/SpoonfulOfBlues)"
redirect_uri = "http://localhost:8080"

# Set up Reddit instance with PRAW
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    redirect_uri=redirect_uri,
)

# Step 1: Generate the authorization URL
auth_url = reddit.auth.url(
    scopes=["identity", "read"], state="unique_state", duration="permanent"
)
print("Authorization URL: ", auth_url)

# Step 2: Ask the user to enter the full URL they get redirected to (containing the authorization code)
response_url = input("Paste the full redirect URL here: ")

# Step 3: Extract the authorization code from the response URL
code = response_url.split("code=")[1].split("#")[0]

# Step 4: Exchange the authorization code for an access token
auth = HTTPBasicAuth(client_id, client_secret)
data = {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri}
headers = {"User-Agent": user_agent}

response = requests.post(
    "https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers
)

# Step 5: Print the response which contains the access token and refresh token
print("Response: ", response.json())

# Optionally extract and print the refresh token
if "refresh_token" in response.json():
    refresh_token = response.json().get("refresh_token")
    print("Your Refresh Token: ", refresh_token)
else:
    print("No Refresh Token found.")


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
