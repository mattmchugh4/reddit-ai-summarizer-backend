import json
import asyncio
from api_request_parallel_processor import process_api_requests_from_file
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")


async def make_async_chatGPT_request():
    open("results.jsonl", "w").close()

    await process_api_requests_from_file(
        requests_filepath="requests_to_process.jsonl",
        save_filepath="results.jsonl",
        request_url="https://api.openai.com/v1/chat/completions",
        api_key="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",
        max_requests_per_minute=1500,
        max_tokens_per_minute=6250000,
        token_encoding_name="cl100k_base",
        max_attempts=5,
        logging_level=20,
    )
    summaries = []
    comments = []
    with open("results.jsonl", "r") as f:
        for line in f:
            response = json.loads(line)
            comments.append(response[0]['messages'][0]['content'])
            summaries.append(response[1]['choices'][0]['message']['content'])
    return {'summaries': summaries, 'comments': comments}




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
        if index > 2:
            break
        index += 1
        joined_comments = "\n".join(comment_chain)

        user_message = chatGPT_question + "\n" + joined_comments

        if len(enc.encode(user_message)) > 3500:
            print('too long')
            continue

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

    return asyncio.run(make_async_chatGPT_request())
