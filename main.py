# from scraper import scraper
import openai


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


print("Type your requests and press Enter. Type 'exit' or 'quit' to exit the program.")

while True:
    print("___________________________________________________________________________________________________________________________________")
    input_message = input("Your request: ")

    if input_message.lower() in ["exit", "quit"]:
        break

    response_message = send_request(input_message)
    print()
    print()
    print(f"ChatGPT API responded: {response_message}")
    print()
