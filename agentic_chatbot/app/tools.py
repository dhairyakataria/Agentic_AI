import os
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.tools.tavily_search import TavilySearchResults
import numexpr as ne
from langchain.tools import tool


def build_tools():
    # ArXiv
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=2)
    arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)


    # Wikipedia
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1)
    wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)


    # Tavily (search tool that uses tavily_api_key)
    tavily_key = os.getenv("TAVILY_KEY")
    search_tool = TavilySearchResults(
    max_results=5,
    include_raw_content=True,
    tavily_api_key=tavily_key,
    )


    # Calculator (wrapped as a langchain tool-style function)
    @tool
    def calculator(expr: str) -> str:
        try:
            result = ne.evaluate(expr)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"


    return [wiki_tool, search_tool, arxiv_tool, calculator]