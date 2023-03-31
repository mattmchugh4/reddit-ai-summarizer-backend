
from bs4 import BeautifulSoup
import requests

# Replace this URL with the URL of the forum page you want to scrape
url = "https://terrylove.com/forums/index.php?threads/should-i-have-re-heated-the-valve.104529/"

# Send a request to the forum page
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")
# text_elements = soup.find_all(text=True)
# print(soup)

# Filter out unwanted elements like styles, scripts, and document tags
# filtered_elements = [element for element in text_elements if element.parent.name not in [
#     'style', 'script', 'head', 'title', 'meta', '[document]']]

# Print the filtered text elements line by line
comment_elements = soup.find_all("div", class_="bbWrapper")

# # Iterate through the comment elements and print the text content
for comment_element in comment_elements:
    comment_text = comment_element.text.strip()
    print(f"User comment: {comment_text}\n")
# # Find all the comment elements on the page
# comment_elements = soup.find_all("div", class_="_1qeIAgB0cPwnLhDF9XSiJM")

# # Iterate through the comment elements and print the text content
# for comment_element in comment_elements:
#     comment_text = comment_element.text.strip()
#     print(f"User comment: {comment_text}\n")
