"""
Tests for MCP client integration.
"""
import pytest
from unittest.mock import AsyncMock, patch
from backend.integrations.mcp_client import MCPClient, MCPConfig
from backend.integrations.google_drive import GoogleDriveAdapter

@pytest.fixture
def mock_config():
    return MCPConfig(
        base_url="https://test-mcp.example.com",
        api_key="test-api-key",
        timeout=30
    )

@pytest.fixture
def mock_client(mock_config):
    return MCPClient(mock_config)

@pytest.mark.asyncio
async def test_google_drive_integration(mock_client):
    """Test Google Drive integration through MCP client"""
    test_doc_id = "test-doc-123"
    expected_response = {
        "content": "Test content",
        "metadata": {"id": test_doc_id}
    }

    with patch('backend.integrations.google_drive.GoogleDriveAdapter.get_document', 
              new_callable=AsyncMock) as mock_get:
        mock_get.return_value = expected_response

        result = await mock_client.get_documents(
            "google-drive",
            {"document_id": test_doc_id}
        )
        assert result == expected_response
        mock_get.assert_called_once()
