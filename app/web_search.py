import logging
import urllib.parse

import bs4
import requests
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)


# none of this is used, idk what I should do with it, maybe delete it
def get_google_search_results(url):
    logger.info(f"Starting search with URL: {url}")

    # Generate a User-Agent header
    try:
        user_agent = UserAgent()
        headers = {"User-Agent": user_agent.chrome}
        logger.debug(f"Using headers: {headers}")
    except Exception as e:
        logger.error(f"Failed to generate User-Agent: {e}")
        return []

    # Make the HTTP request
    try:
        logger.info("Sending GET request to Google")
        request_result = requests.get(url, headers=headers, timeout=10)
        request_result.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        logger.debug(f"Response status code: {request_result.status_code}")
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        print(e)
        return []

    # Parse the HTML response
    try:
        soup = bs4.BeautifulSoup(request_result.text, "html.parser")
        logger.debug(
            f"HTML content received (first 500 characters): {soup.prettify()[:500]}"
        )
    except Exception as e:
        logger.error(f"Failed to parse HTML content: {e}")
        return []

    # Find link spans in the parsed HTML
    try:
        # print(soup)
        link_spans = soup.find_all("span", {"class": "CVA68e qXLe6d fuLhoc ZWRArf"})
        logger.debug(f"Found {len(link_spans)} spans with the target class.")
    except Exception as e:
        logger.error(f"Error while finding spans: {e}")
        return []

    results = []
    print(link_spans)

    # Extract links from the spans
    for idx, span in enumerate(link_spans):
        try:
            a_tag = span.find_parent("a")
            if not a_tag or "href" not in a_tag.attrs:
                logger.warning(
                    f"Span #{idx} does not have a valid parent <a> tag. Skipping."
                )
                continue

            url = a_tag["href"]
            clean_url = url.split("/url?q=")[1].split("&sa=")[0]
            logger.debug(f"Extracted URL: {clean_url}")

            results.append((span.getText(), clean_url))
        except IndexError as e:
            logger.warning(f"Failed to parse URL for span #{idx}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for span #{idx}: {e}")

    logger.info(f"Returning {len(results)} results")
    return results


def perform_search(search_query):
    query = urllib.parse.quote_plus(search_query)
    url = f"https://www.google.com/search?q={query}+site:reddit.com&oq={query}+site:reddit.com&aqs=chrome.0.35i39l2j0l4j46j69i60.1467j0j7&sourceid=chrome&ie=UTF-8"
    results = get_google_search_results(url)

    return results


# print(perform_search("this is a test"))

# def get_google_search_results(url):
#     user_agent = UserAgent()
#     headers = {'User-Agent': user_agent.chrome}

#     request_result = requests.get(url, headers=headers)
#     # request_result = requests.get(url)

#     soup = bs4.BeautifulSoup(request_result.text, 'html.parser')
#     heading_object = soup.find_all('h3')
#     print(soup)

#     results = []

#     for info in heading_object:
#         a_tag = info.find_parent('a')
#         url = a_tag['href']
#         clean_url = url.split('/url?q=')[1].split('&sa=')[0]
#         results.append((info.getText(), clean_url))

#     return results
