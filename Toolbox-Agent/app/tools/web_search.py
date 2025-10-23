from langchain.tools import tool
import os
import serpapi

@tool
def web_search(query: str) -> str:
    """Search the web for current information. Use this when you need recent data or facts not in your knowledge."""
    try:
        client = serpapi.Client(api_key=os.getenv("SERPAPI_KEY"))
        search = client.search({
            'engine': 'google',
            'q': query,
        })
        results = search.get_dict()
        
        # Extract top 3 organic results
        snippets = []
        for result in results.get("organic_results", [])[:3]:
            snippets.append(f"- {result['title']}: {result['snippet']}")
        
        return "\n".join(snippets) if snippets else "No results found"
    except Exception as e:
        return f"Search error: {str(e)}"