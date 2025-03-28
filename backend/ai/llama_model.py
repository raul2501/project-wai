"""
AI Service Integration for Wai.
Provides unified interface to external AI services.
"""
from typing import List, Optional
import httpx
from pydantic import BaseModel

class AIServiceConfig(BaseModel):
    """Configuration for AI service"""
    base_url: str
    api_key: str
    model: str = "gpt-4"
    timeout: int = 30

class AIServiceClient:
    """Client for interacting with external AI services."""
    
    def __init__(self, config: AIServiceConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            headers={"Authorization": f"Bearer {config.api_key}"},
            timeout=config.timeout
        )
    
    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the AI service.
        
        Args:
            prompt: The input text prompt
            
        Returns:
            String containing the AI's response
        """
        try:
            response = await self.client.post(
                "/v1/completions",
                json={
                    "model": self.config.model,
                    "prompt": prompt,
                    "max_tokens": 1024
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["text"]
        except Exception as e:
            raise Exception(f"AI service error: {str(e)}")
    
    async def process_documents(self, documents: List[str], query: Optional[str] = None) -> str:
        """
        Process document content and generate a response.
        
        Args:
            documents: List of document content strings
            query: Optional query to ask about the documents
            
        Returns:
            String containing the AI's response about the documents
        """
        combined_docs = "\n\n---\n\n".join(documents)
        prompt = (
            f"Below are documents:\n\n{combined_docs}\n\n"
            f"{query if query else 'Summarize the key information'}"
        )
        return await self.generate_response(prompt)
