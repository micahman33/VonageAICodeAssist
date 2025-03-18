# Vonage AI Assist MCP Server

## Overview

Vonage Assist is a Model Context Protocol (MCP) server designed to help developers integrate Vonage API capabilities into their applications. The server leverages FastMCP to provide AI-assisted access to Vonage documentation, enabling developers to quickly find relevant information about Vonage's communication APIs.

## How It Works

The Vonage Assist MCP server operates as follows:

1. **Documentation Search**: The server provides a specialized tool called "Vonage-Assist" that searches through Vonage's official documentation.

2. **Web Search Integration**: Using the Google Serper API, the tool performs targeted searches within the Vonage developer documentation domain (`developer.vonage.com/en/documentation`).

3. **Content Extraction**: When a search query is submitted, the server:
   - Formulates a site-specific search query
   - Sends the query to Google Serper API
   - Receives search results with relevant documentation links
   - Fetches the content from these links
   - Returns the extracted text content to the user

4. **MCP Tool Integration**: The server is compatible with Claude and other AI assistants that support the MCP protocol, allowing these AI systems to directly utilize Vonage documentation in their responses.

## Setup & Requirements

To run the Vonage Assist MCP server:

1. Ensure Python 3.13+ is installed.

2. Set up the required environment variables:
   - `SERPER_API_KEY`: API key for Google Serper (required for web searches)

3. Install dependencies:
   ```bash
   uv install
   ```

4. Run the server:
   ```bash
   python main.py
   ```

## Usage

Once running, the MCP server exposes the `Vonage-Assist` tool with the following parameters:

- `query`: The search query (e.g., "number verification", "SMS API")
- `library`: The documentation library to search ("vonage" is currently the only supported option)

Example tool usage (via an MCP-compatible AI):
```
Use the Vonage-Assist tool to find information about implementing two-factor authentication with Vonage APIs.
```

## Technical Implementation

The server is built using:
- FastMCP for the MCP server framework
- httpx for asynchronous HTTP requests
- BeautifulSoup for HTML parsing and text extraction
- python-dotenv for environment variable management

The core functionality is implemented through several key functions:
- `search_web()`: Performs API requests to Google Serper
- `fetch_url()`: Retrieves and extracts content from web pages
- `vonage_docs()`: The main tool function that orchestrates the search and content retrieval process

## Future Considerations

Top potential enhancements for the Vonage Assist MCP server:

1. **Code Generation Tool**: Add capabilities to generate sample code snippets for common Vonage API integrations (SMS, Voice, Verify, Video) in multiple programming languages, helping developers quickly implement Vonage features with proper syntax and best practices.

2. **API Parameter Helper**: Develop a tool that helps developers construct valid API requests by suggesting parameters, validating inputs, and explaining required vs. optional fields for different Vonage API endpoints.

3. **Troubleshooting Assistant**: Implement functionality to diagnose common integration issues by analyzing error codes and providing actionable solutions based on KB articles and documentation - significantly reducing debugging time.

4. **Webhook Configuration Helper**: Create a tool to assist with setting up and testing webhook endpoints for Vonage services, guiding developers through the process of handling callbacks and events.

5. **Best Practices Advisor**: Add a capability to provide context-specific best practices for performance, security, and resilience when implementing Vonage APIs, helping developers build more robust applications.

6. **Rate Limit & Pricing Estimator**: Help developers estimate costs and understand rate limits for their specific use cases.
