import requests


def extract_source(url, proxies=None):
    agent = {"User-Agent": "Chrome"}
    source = requests.get(url, headers=agent, proxies=proxies).text
    return source
