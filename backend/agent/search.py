from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from core.config import settings

wrapper = DuckDuckGoSearchAPIWrapper(region="ru-ru", time="y", source="text", max_results=settings.web_max_results)
web_search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)
