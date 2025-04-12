"""
MCP (Model Context Processor) Client for Wai.
Provides unified interface to various MCP integrations.
"""
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel
from backend.integrations.google_drive import GoogleDriveConfig

class MCPConfig(BaseModel):
    """Configuration for MCP service"""
    base_url: str
    api_key: str
    timeout: int = 30

class MCPClient:
    """Client for interacting with MCP services."""
    
    def __init__(self, config: MCPConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            headers={"Authorization": f"Bearer {config.api_key}"},
            timeout=config.timeout
        )
    
    async def get_documents(self, source: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get documents from specified MCP integration.
        
        Args:
            source: Integration type (e.g. 'google-drive')
            params: Source-specific parameters
            
        Returns:
            Dictionary containing documents and metadata
        """
        if source == "google-drive":
            from backend.integrations.google_drive import GoogleDriveAdapter
            adapter = GoogleDriveAdapter(GoogleDriveConfig(
                base_url=f"{self.config.base_url}/google-drive",
                api_key=self.config.api_key,
                timeout=self.config.timeout
            ))
            return await adapter.get_document(params["document_id"])
        else:
            try:
                response = await self.client.post(
                    f"/v1/{source}/documents",
                    json=params
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                raise Exception(f"MCP {source} error: {str(e)}")

    async def list_files(self, source: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List files from the specified MCP integration.

        Args:
            source: Integration type (e.g., 'google-drive')
            params: Source-specific parameters (e.g., folder_id).

        Returns:
            Dictionary containing a list of files and their metadata.
        """
        if source == "google-drive":
            from backend.integrations.google_drive import GoogleDriveAdapter
            adapter = GoogleDriveAdapter(GoogleDriveConfig(
                base_url=f"{self.config.base_url}/google-drive",
                api_key=self.config.api_key,
                timeout=self.config.timeout
            ))
            return await adapter.list_files(params.get("folder_id"))
        else:
            raise Exception(f"Listing files is not supported for source: {source}")
    
    
async def get_metadata(self, source: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch metadata for a specific file from the specified MCP integration.

    Args:
        source: Integration type (e.g., 'google-drive')
        params: Source-specific parameters (e.g., file_id).

    Returns:
        Dictionary containing file metadata.
    """
    if source == "google-drive":
        from backend.integrations.google_drive import GoogleDriveAdapter
        adapter = GoogleDriveAdapter(GoogleDriveConfig(
            base_url=f"{self.config.base_url}/google-drive",
            api_key=self.config.api_key,
            timeout=self.config.timeout
        ))
        return await adapter.get_metadata(params["file_id"])
    else:
        raise Exception(f"Fetching metadata is not supported for source: {source}")
    
    # Add other MCP methods as needed
