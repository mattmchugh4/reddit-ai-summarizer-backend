import json
import asyncio
from api_request_parallel_processor import process_api_requests_from_file


async def make_async_chatGPT_request():
    await process_api_requests_from_file(
        requests_filepath="requests_to_process.jsonl",
        save_filepath="results.jsonl",
        request_url="https://api.openai.com/v1/engines/gpt-3.5-turbo/completions",
        api_key="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",
        max_requests_per_minute=1500,
        max_tokens_per_minute=6250000,
        token_encoding_name="cl100k_base",
        max_attempts=5,
        logging_level=20,
    )
{"prompt":
    "Can you concisely summarize the main points for the Reddit comment chain that is pasted below?\nCOMMENT (21): Basically Any car from Toyota.", "max_tokens": 50, "temperature": 0.7}


def format_chatGPT_inputs(comment_array):

    chatGPT_summaries = []

    chatGPT_question = 'Can you concisely summarize the main points for the Reddit comment chain that is pasted below?' \
        # f'This comment chain is in response to a post titled: {comments["title"]};.'
    # f'This comment chain is in response to a post ,  Title: {comments["title"]}; Body: {comments["initial_post"]}.'


    formatted_requests = []
    index = 0
    for comment_chain in comment_array:
        if len(comment_chain) == 0:
            continue
        if index > 3:
            break
        index += 1
        joined_comments = "\n".join(comment_chain)

        user_message = chatGPT_question + "\n" + joined_comments
        # print(prompt)
        request_object = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        formatted_requests.append(request_object)

    with open("requests_to_process.jsonl", "w") as outfile:
        for request in formatted_requests:
            outfile.write(json.dumps(request) + "\n")

    asyncio.run(make_async_chatGPT_request())

    # prompts = []

    # for comment_chain in comments['formatted_comments']:
    #     if index > 10:
    #         break
    #     index += 1
    #     joined_comments = "\n".join(comment_chain)

    #     prompt = chatGPT_question + "\n" + joined_comments
    #     if len(enc.encode(prompt)) > 3500:
    #         print('too long')
    #         continue
    #     response_object['tokens'] += len(enc.encode(prompt))

    #     summary = send_request(prompt)
    #     response_object['tokens'] += len(enc.encode(summary))

    #     chatGPT_summaries.append(summary)
