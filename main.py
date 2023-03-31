# main.py
import openai
from comment_scraper import scrape_comments

openai.api_key = "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"


def send_request(input_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": input_message}
        ]
    )

    response_message = response.choices[0].message['content'].strip()
    return response_message


print("Enter the Reddit post URL to scrape comments from:")
post_url = input().strip()

# Scrape comments from the provided URL
comments = scrape_comments(post_url)

# Print the scraped comments
print("\nScraped comments:")
print(comments)

print("\nEnter your question for ChatGPT, or type 'exit' or 'quit' to exit the program.")
while True:
    input_message = input("Your question: ")
    if input_message.lower() in ["exit", "quit"]:
        break

    # Append the scraped comments to the question
    input_message_with_comments = input_message + " " + comments

    response_message = send_request(input_message_with_comments)
    print(f"\nChatGPT API responded: {response_message}\n")
