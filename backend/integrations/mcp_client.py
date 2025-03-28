"""
MCP (Microservice Control Plane) Client for Wai.
Provides unified interface to various MCP integrations.
"""
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel

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
        try:
            response = await self.client.post(
                f"/v1/{source}/documents",
                json=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"MCP {source} error: {str(e)}")

    # Add other MCP methods as needed
