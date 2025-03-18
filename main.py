from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import json
import os
import sys
from bs4 import BeautifulSoup
from typing import Dict, Optional, List

# Constants
SERPER_URL = "https://google.serper.dev/search"
SEARCH_RESULTS_LIMIT = 5
REQUEST_TIMEOUT = 30.0
DOCS_URLS = {
    "vonage": "developer.vonage.com/en/documentation",
}

async def search_web(query: str) -> Dict:
    """
    Search for content using Google Serper API.
    
    Args:
        query: The search query string
        
    Returns:
        Dictionary containing search results
    """
    payload = json.dumps({"q": query, "num": SEARCH_RESULTS_LIMIT})
    
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_URL, headers=headers, data=payload, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except (httpx.TimeoutException, httpx.HTTPStatusError):
            return {"organic": []}

async def fetch_url(url: str) -> str:
    """
    Fetch content from a URL and extract the text.
    
    Args:
        url: The URL to fetch
        
    Returns:
        Extracted text content
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text()
        except (httpx.TimeoutException, httpx.HTTPStatusError):
            return "Error: Unable to fetch content"

def create_mcp_server() -> FastMCP:
    """Create and configure the MCP server."""
    return FastMCP("vonageassist")

def main():
    """Initialize and run the Vonage Assist MCP server."""
    # Load environment variables
    load_dotenv()
    
    # Check for required API key
    if not os.getenv("SERPER_API_KEY"):
        print("Error: SERPER_API_KEY not found in environment", file=sys.stderr)
        sys.exit(1)
    
    # Create MCP server
    mcp = create_mcp_server()
    
    @mcp.tool("Vonage-Assist")
    async def vonage_docs(query: str, library: str) -> str:
        """
        Search through the latest Vonage documentation and code samples
        to find relevant references for AI generated code on the newest
        and best platform capabilities

        Args:
            query: The query to search for (e.g. "number verification")
            library: The library to search in (e.g. "vonage") - "vonage" is currently the only supported library.
                    Future to include additional code references

        Returns:
            Text from the docs
        """
        # Validate library parameter
        if library not in DOCS_URLS:
            raise ValueError(f"Library {library} not supported by this tool")
        
        # Construct site-specific search query
        site_query = f"site:{DOCS_URLS[library]} {query}"
        
        # Perform search
        results = await search_web(site_query)
        if not results.get("organic", []):
            return "No results found"
        
        # Fetch and combine content from all results
        content_parts = []
        for result in results["organic"]:
            content = await fetch_url(result["link"])
            content_parts.append(content)
        
        return "\n\n---\n\n".join(content_parts)
    
    # Run the server
    mcp.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error initializing server: {str(e)}", file=sys.stderr)
        raise