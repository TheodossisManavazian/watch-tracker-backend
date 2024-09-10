import requests
from requests_html import HTMLSession


def extract_source(url, proxies=None):
    agent = {"User-Agent": "Chrome"}
    source = requests.get(url, headers=agent, proxies=proxies).text
    return source


def extract_source_using_requests_html(session, url):
    response = session.get(url)
    response.html.render(sleep=1)
    return response.html.html
