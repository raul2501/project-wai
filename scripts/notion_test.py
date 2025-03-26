"""
Notion API integration for Wai.
Provides functionality to access and extract data from Notion pages.
"""
from notion_client import Client
import sys
import os

# Add the parent directory to the path so we can import from config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.notion_config import (
    NOTION_API_TOKEN, 
    DEFAULT_PAGE_ID,
    TEXT_BLOCK_TYPES
)

def get_notion_client():
    """Initialize and return a Notion client with configured API token."""
    return Client(auth=NOTION_API_TOKEN)

def extract_text(blocks):
    """
    Extract text content from Notion blocks.
    
    Args:
        blocks: The blocks data returned from Notion API
        
    Returns:
        String containing the concatenated text content
    """
    texts = []
    for block in blocks.get("results", []):
        block_type = block.get("type")
        # Check if the block type has a "rich_text" field
        if block_type in TEXT_BLOCK_TYPES:
            rich_text_list = block.get(block_type, {}).get("rich_text", [])
            # Concatenate all text content in this block
            block_text = "".join([text_obj.get("text", {}).get("content", "") 
                                for text_obj in rich_text_list])
            texts.append(block_text)
        # You can add additional handling for other block types if needed
    return "\n".join(texts)

def search_notion(query="", filter_type=None):
    """
    Search Notion for pages matching the query.
    
    Args:
        query: Search query string
        filter_type: Optional filter (e.g., "page", "database")
        
    Returns:
        List of search results
    """
    notion = get_notion_client()
    search_params = {"query": query}
    
    if filter_type:
        search_params["filter"] = {"property": "object", "value": filter_type}
        
    response = notion.search(**search_params)
    return response["results"]

def get_page_content(page_id=DEFAULT_PAGE_ID):
    """
    Retrieve and extract text content from a Notion page.
    
    Args:
        page_id: ID of the Notion page to retrieve
        
    Returns:
        String containing the page's text content
    """
    notion = get_notion_client()
    page_content = notion.blocks.children.list(block_id=page_id)
    return extract_text(page_content)

if __name__ == "__main__":
    # Example usage
    notion = get_notion_client()
    
    # Uncomment to search Notion
    # results = search_notion("your search query")
    # for result in results:
    #     print(f"ID: {result['id']}, Title: {result['properties'].get('title', {}).get('title', [{}])[0].get('text', {}).get('content', 'No Title')}")
    
    # Get page content
    clean_text = get_page_content()
    print(clean_text)