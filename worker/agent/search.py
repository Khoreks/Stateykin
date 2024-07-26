import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

load_dotenv()

search = GoogleSearchAPIWrapper()


def extract_information(url):
    try:
        response = requests.get(url, timeout=3)
    except:
        return {
            "error": "connections error"
        }
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.replace("\xa0", " ") if soup.title else "No title found"
        paragraphs = [p.text.replace("\xa0", ' ') for p in soup.find_all("p")]
        try:
            paragraphs = [p.decode('utf-8') for p in paragraphs]
        except:
            pass
        return {
            "title": title,
            "paragraphs": paragraphs
        }
    else:
        return {
            "error": f"Failed to retrieve the page. Status code: {response.status_code}"
        }


def web_search(queries: list):
    content = []
    for query in queries:
        query += " -cyberleninka -youtube -rutube -видео -pdf -instagram -facebook -twitter"
        search_results = search.results(query, 2)

        content.append([extract_information(page.get("link", None)) for page in search_results])

    return content


web_search_tool = Tool(
    name="Google Search",
    description="Google page search with content parsing",
    func=web_search,
)
