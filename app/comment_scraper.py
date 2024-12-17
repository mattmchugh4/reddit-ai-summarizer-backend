from datetime import datetime


def format_comment(comment, depth=0):

    if comment.body in ["[deleted]", "[removed]"]:
        return []

    if depth > 5 or comment.score <= -3:
        return []

    if depth == 0:
        formatted_comment = [f"COMMENT ({comment.score}): {comment.body}"]
    else:
        formatted_comment = [f"REPLY {depth} ({comment.score}): {comment.body}"]

    if depth < 5:
        for reply in comment.replies:
            formatted_comment.extend(format_comment(reply, depth + 1))

    return formatted_comment


def scrape_comments(reddit, post_url):
    post_id = post_url.split("/")[-3]

    post = reddit.submission(id=post_id)

    # Replace "more_comments" with actual comments
    post.comments.replace_more(limit=None)

    post_data = {}
    formatted_comments = []
    comment_string_split = []
    comment_string = ""

    for comment in post.comments:
        comment_string += "__break__\n"
        new_comment_chain = format_comment(comment)
        formatted_comments.append(new_comment_chain)

        for new_comment in new_comment_chain:
            comment_string += new_comment + " "

        comment_string += "\n"

    comment_string_split.append(comment_string)

    post_data["title"] = post.title
    post_data["initial_post"] = post.selftext

    post_date = post.created_utc

    post_date_formatted = datetime.utcfromtimestamp(post_date).strftime("%m/%d/%Y")

    post_data["post_date"] = post_date_formatted

    post_data["formatted_comments"] = formatted_comments
    post_data["comment_strings"] = comment_string_split

    return post_data
