import requests
from config import COURTLISTENER_API_URL

def fetch_cases(query: str):
    params = {"q": query, "type": "case"}
    response = requests.get(COURTLISTENER_API_URL, params=params)

    if response.status_code == 200:
        cases = response.json().get("results", [])
        return [
            {
                "title": case.get("caseName"),
                "summary": case.get("summary", "No summary available."),
                "citation": case.get("citation"),
                "url": case.get("absolute_url", "")
            }
            for case in cases
        ]
    return []