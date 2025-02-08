import requests
import os

API_URL = "https://www.courtlistener.com/api/rest/v3/opinions/"
API_KEY = os.getenv("COURTLISTENER_API_KEY")

def fetch_case_law(keywords: str, jurisdiction: str):
    headers = {"Authorization": f"Token {API_KEY}"}
    params = {"search": keywords, "jurisdiction": jurisdiction}

    response = requests.get(API_URL, headers=headers, params=params)
    data = response.json()

    if data["results"]:
        case = data["results"][0]
        return {
            "title": case["caseName"],
            "citation": case["citations"][0]["cite"],
            "jurisdiction": case["jurisdiction"],
            "summary": case["plain_text"],
            "full_text_url": case["absolute_url"],
        }
    return None
