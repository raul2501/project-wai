"""
Configuration for Google Drive MCP integration.
"""
from pydantic import BaseModel

class GoogleDriveMCPConfig(BaseModel):
    """Google Drive MCP configuration"""
    base_url: str = "https://mcp.yourdomain.com/google-drive"
    api_key: str = "your-google-drive-mcp-api-key"
    default_document_fields: list = ["id", "name", "mimeType", "modifiedTime"]
    timeout: int = 30
