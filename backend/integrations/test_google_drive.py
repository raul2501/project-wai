"""
Tests for Google Drive MCP integration.
"""
import pytest
from unittest.mock import AsyncMock, patch
from backend.integrations.google_drive import GoogleDriveAdapter, GoogleDriveConfig

@pytest.fixture
def mock_config():
    return GoogleDriveConfig(
        base_url="https://test-mcp.example.com",
        api_key="test-api-key",
        timeout=30
    )

@pytest.fixture
def mock_adapter(mock_config):
    return GoogleDriveAdapter(mock_config)

@pytest.mark.asyncio
async def test_get_document_success(mock_adapter):
    """Test successful document retrieval"""
    test_doc_id = "test-doc-123"
    expected_response = {
        "content": "Test document content",
        "metadata": {"id": test_doc_id}
    }

    with patch.object(mock_adapter.client, 'post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = expected_response

        result = await mock_adapter.get_document(test_doc_id)
        assert result == expected_response
        mock_post.assert_called_once_with(
            "/v1/documents/get",
            json={"document_id": test_doc_id}
        )

@pytest.mark.asyncio
async def test_get_document_error(mock_adapter):
    """Test error handling in document retrieval"""
    test_doc_id = "test-doc-123"

    with patch.object(mock_adapter.client, 'post', new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = Exception("Test error")

        with pytest.raises(Exception) as exc_info:
            await mock_adapter.get_document(test_doc_id)
        assert "Google Drive MCP error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_search_documents_success(mock_adapter):
    """Test successful document search"""
    test_query = "important"
    expected_response = {
        "results": [{"id": "doc1"}, {"id": "doc2"}]
    }

    with patch.object(mock_adapter.client, 'post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = expected_response

        result = await mock_adapter.search_documents(test_query)
        assert result == expected_response
        mock_post.assert_called_once_with(
            "/v1/documents/search",
            json={"query": test_query}
        )
