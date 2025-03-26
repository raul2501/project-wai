"""
Configuration file for Notion API integration.
"""

# Notion API token (replace with your actual token)
# You can get this from https://www.notion.so/my-integrations
NOTION_API_TOKEN = "ntn_j72379446949ZdYH99mIX057txRMoUjqAEHpoZMgfLAe7G"

# Default page/block ID to access 
DEFAULT_PAGE_ID = "1be1af6a45768035905ac66f75fd004f"

# Content block types to extract text from
TEXT_BLOCK_TYPES = [
    "paragraph", 
    "heading_1", 
    "heading_2", 
    "heading_3",
    "bulleted_list_item", 
    "numbered_list_item", 
    "toggle"
]

# Advanced configuration settings
MAX_RESULTS_PER_REQUEST = 100  # Number of results to return in search queries