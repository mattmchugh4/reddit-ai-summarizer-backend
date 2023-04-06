import tiktoken


comments = "Or getting something like a Lexus LS series(even though it's barely a luxury car in comparison to a 7 series/S class) or the newer Genesis isn't a bad idea for long term running costs.Comment 2 (7): Lexus LS is an exception. I’m biased"




enc = tiktoken.get_encoding("cl100k_base")
tokens = enc.encode(comments)
print('Number of Tokens:', str(len(tokens)))
