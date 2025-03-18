from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import json
import os
import sys
from bs4 import BeautifulSoup

try:
    load_dotenv()
    
    if not os.getenv("SERPER_API_KEY"):
        print("Error: SERPER_API_KEY not found in environment", file=sys.stderr)
        sys.exit(1)
        
    mcp = FastMCP("vonageassist")

    USER_AGENT = "docs-app/1.0"
    SERPER_URL="https://google.serper.dev/search"

    docs_urls = {
        "vonage": "developer.vonage.com/en/documentation",
    }

    # # Register a tool
    # @mcp.tool("search_docs")
    # async def search_docs(query: str) -> str:
    #     """Search documentation across multiple sources."""
    #     results = await search_web(query)
    #     return json.dumps(results, indent=2)

    async def search_web(query: str) -> dict | None:
        payload = json.dumps({"q": query, "num": 2})

        headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    SERPER_URL, headers=headers, data=payload, timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.TimeoutException:
                return {"organic": []}
    
    async def fetch_url(url: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()
                return text
            except httpx.TimeoutException:
                return "Timeout error"


    # Converts the function definition to a tool that's compatible with MCP def
    # Docs string is what appears to the user when they see this MCP tool
    # This is also the description used by the LLM to determine when this tool is useful
    # If its not specific enough, the agent wont be able to find it
    @mcp.tool("Vonage-Assist")
    async def vonage_docs(query: str, library: str):
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
        if library not in docs_urls:
            raise ValueError(f"Library {library} not supported by this tool")
        
        query = f"site:{docs_urls[library]} {query}"
        results = await search_web(query)
        if len(results["organic"]) == 0:
            return "No results found"
        
        text = ""
        for result in results["organic"]:
            text += await fetch_url(result["link"])
        return text


    if __name__ == "__main__":
        mcp.run()
except Exception as e:
    print(f"Error initializing server: {str(e)}", file=sys.stderr)
    raise