import json

import requests


def get_news(api_key: str, query: str, language: str = "en"):
    url = f"https://newsdata.io/api/1/news"
    headers = {
        "X-ACCESS-KEY": api_key,
    }
    params = {
        "q": query,
        "language": language,
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")


def save_output(content):
    with open("news.json", "w") as file:
        json.dump(content, file, indent=2)


def mock_make_request():
    with open("news.json") as file:
        return json.load(file)
