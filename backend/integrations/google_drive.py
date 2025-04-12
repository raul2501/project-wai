"""
Google Drive MCP Adapter for Wai.
Handles Google Drive-specific document operations.
"""
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel

class GoogleDriveConfig(BaseModel):
    """Google Drive specific configuration"""
    base_url: str = "https://mcp.yourdomain.com/google-drive"
    api_key: str
    timeout: int = 30

class GoogleDriveAdapter:
    """Adapter for Google Drive operations via MCP"""
    
    def __init__(self, config: GoogleDriveConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            },
            timeout=config.timeout
        )
    
    async def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document content from Google Drive"""
        try:
            response = await self.client.post(
                "/v1/documents/get",
                json={"document_id": document_id}
            )
            response.raise_for_status()
            return await response.json()
        except Exception as e:
            raise Exception(f"Google Drive MCP error: {str(e)}")

    async def search_documents(self, query: str) -> Dict[str, Any]:
        """Search documents in Google Drive"""
        try:
            response = await self.client.post(
                "/v1/documents/search",
                json={"query": query}
            )
            response.raise_for_status()
            return await response.json()
        except Exception as e:
            raise Exception(f"Google Drive search error: {str(e)}")
        
    async def list_files(self, folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        List files in a folder or root directory.

        Args:
            folder_id: ID of the folder to list files from (optional).

        Returns:
            Dictionary containing a list of files and their metadata.
        """
        params = {
            "q": f"'{folder_id}' in parents" if folder_id else None,
            "fields": "files(id, name, mimeType, modifiedTime)"
        }
        try:
            response = await self.client.get("/files", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error listing files in Google Drive: {str(e)}")
        
    async def get_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Fetch metadata for a specific file.

        Args:
            file_id: ID of the file to fetch metadata for.

        Returns:
            Dictionary containing file metadata.
        """
        try:
            response = await self.client.get(f"/files/{file_id}", params={
                "fields": "id, name, mimeType, size, modifiedTime"
            })
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise Exception(f"Failed to fetch metadata: {str(e)}")
