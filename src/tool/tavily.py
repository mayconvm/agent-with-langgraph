import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
import dotenv

dotenv.load_dotenv()

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """
    Search the internet for information using the Tavily API.

    Args:
        query (str): The search query to execute.
        max_results (int, optional): The maximum number of search results to return. Defaults to 5.
        topic (Literal["general", "news", "finance"], optional): The category of search to perform (general, news, or finance). Defaults to "general".
        include_raw_content (bool, optional): Whether to include the full raw content of the search results. Defaults to False.
    """
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
