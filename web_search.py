import urllib.parse
import requests
import bs4
import urllib.parse
from fake_useragent import UserAgent


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

def get_google_search_results(url):
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.chrome}

    request_result = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(request_result.text, 'html.parser')

    link_spans = soup.find_all(
        'span', {'class': 'CVA68e qXLe6d fuLhoc ZWRArf'})

    results = []

    for span in link_spans:
        a_tag = span.find_parent('a')
        url = a_tag['href']
        clean_url = url.split('/url?q=')[1].split('&sa=')[0]
        results.append((span.getText(), clean_url))

    return results


def perform_search(search_query):
    query = urllib.parse.quote_plus(search_query)
    url = f"https://www.google.com/search?q={query}+site:reddit.com&oq={query}+site:reddit.com&aqs=chrome.0.35i39l2j0l4j46j69i60.1467j0j7&sourceid=chrome&ie=UTF-8"
    results = get_google_search_results(url)
    return results
