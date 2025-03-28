"""
Document API endpoints for Wai.
Handles document retrieval and processing.
"""
from typing import Dict, List, Any, Optional, Union
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from backend.integrations.mcp_client import MCPClient, MCPConfig
from backend.ai.llama_model import AIServiceClient, AIServiceConfig
from pydantic import BaseModel

router = APIRouter()

# Configuration would typically come from environment variables
mcp_config = MCPConfig(
    base_url="https://mcp.yourdomain.com",
    api_key="your-mcp-api-key"
)

ai_config = AIServiceConfig(
    base_url="https://ai.yourdomain.com",
    api_key="your-ai-api-key"
)

mcp_client = MCPClient(mcp_config)
ai_client = AIServiceClient(ai_config)

class DocumentRequest(BaseModel):
    """Document request schema."""
    source: str  # e.g. 'google-drive'
    params: Dict[str, Any]  # Source-specific parameters
    query: Optional[str] = None

class DocumentResponse(BaseModel):
    """Document response schema."""
    content: Dict[str, Any]  # Raw document data
    ai_response: Optional[str] = None


@router.post("/process", response_model=DocumentResponse)
async def process_document_endpoint(request: DocumentRequest):
    """
    Process a document and generate AI response.
    
    Args:
        request: Document request with source, ID, and optional query
        
    Returns:
        Document content and AI-generated response
    """
    try:
        # Get document from MCP service
        doc_data = await mcp_client.get_documents(request.source, request.params)
        content = doc_data.get('content', '')
        
        # Generate AI response if content was retrieved successfully
        if content:
            ai_response = await ai_client.process_documents([content], request.query)
        else:
            ai_response = "No content to analyze"
        
        return DocumentResponse(
            content=formatted_content[:1000] + "..." if len(formatted_content) > 1000 else formatted_content,
            ai_response=ai_response
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.post("/batch_process")
async def batch_process_documents(requests: List[DocumentRequest]):
    """
    Process multiple documents and generate a combined AI response.
    
    Args:
        requests: List of document requests
        
    Returns:
        AI-generated response based on all documents
    """
    try:
        documents = []
        
        # Process each document
        for request in requests:
            doc_data = await mcp_client.get_documents(request.source, request.params)
            content = doc_data.get('content', '')
            
            if content:
                documents.append(content)
        
        # Generate combined AI response
        if documents:
            query = requests[0].query if requests and requests[0].query else None
            ai_response = await ai_client.process_documents(documents, query)
        else:
            ai_response = "No content to analyze"
        
        return {"ai_response": ai_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")
