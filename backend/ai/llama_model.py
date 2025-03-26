"""
Llama-3 integration for Wai.
Provides functionality to interact with Llama-3 models via API.
"""
import os
import json
import torch
from typing import Dict, List, Any, Optional, Union
from transformers import AutoModelForCausalLM, AutoTokenizer


class LlamaModel:
    """Client for interacting with Llama-3 models."""
    
    def __init__(self, model_name: str = "meta-llama/Llama-3-8B-Instruct", token: str = None):
        """Initialize Llama model and tokenizer."""
        self.model_name = model_name
        
        # Force CPU for testing to avoid device-related issues
        self.device = "cpu"
        
        try:
            print(f"Loading model {model_name} on {self.device}...")
            # Pass token to from_pretrained if provided
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, 
                torch_dtype=torch.float32,
                device_map=None,  # Don't use device_map for better control
                token=token  # Pass token here too
            )
            # Explicitly move model to CPU
            self.model.to(self.device)
            print(f"Model loaded successfully")
        except Exception as e:
            print(f"Error loading model {model_name}: {str(e)}")
            print("If this is a gated model, you need to provide a Hugging Face token.")
            print("Falling back to a smaller open-access model...")
            
            # Fall back to a more stable freely available model
            self.model_name = "gpt2"  # Small model that's freely available and more stable
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            # Set pad token for GPT-2 which doesn't have one by default
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                device_map=None  # Don't use device_map for better control
            )
            # Make the model aware of the pad token
            self.model.config.pad_token_id = self.model.config.eos_token_id
            # Explicitly move model to CPU
            self.model.to(self.device)
            print(f"Fallback model {self.model_name} loaded successfully")
    
    def generate_response(self, prompt: str, max_length: int = 1024) -> str:
        """
        Generate a response from the model based on input prompt.
        
        Args:
            prompt: The input text prompt
            max_length: Maximum length of generated response
            
        Returns:
            String containing the model's response
        """
        # Format prompt based on model type
        if "opt" in self.model_name.lower():
            # Format for OPT models
            formatted_prompt = f"Human: {prompt}\n\nAssistant: "
        elif "gpt2" in self.model_name.lower():
            # Format for GPT-2
            formatted_prompt = f"Question: {prompt}\nAnswer:"
        else:
            # Format for Llama models
            formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        
        # Tokenize the prompt - simpler approach to avoid padding issues
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.device)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_new_tokens=max_length,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode the response
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the assistant's response based on model type
        if "opt" in self.model_name.lower():
            # Extract response for OPT models
            parts = generated_text.split("Assistant: ")
            if len(parts) > 1:
                response = parts[1].strip()
            else:
                response = generated_text  # Fallback
        elif "gpt2" in self.model_name.lower():
            # Extract response for GPT-2
            parts = generated_text.split("Answer:")
            if len(parts) > 1:
                response = parts[1].strip()
            else:
                response = generated_text  # Fallback
        else:
            # Extract response for Llama models
            parts = generated_text.split("[/INST]")
            if len(parts) > 1:
                response = parts[1].strip()
            else:
                response = generated_text  # Fallback
        
        return response
    
    def process_documents(self, documents: List[str], query: Optional[str] = None) -> str:
        """
        Process document content and generate a response.
        
        Args:
            documents: List of document content strings
            query: Optional query to ask about the documents
            
        Returns:
            String containing the model's response about the documents
        """
        # Join documents with separator
        combined_docs = "\n\n---\n\n".join(documents)
        
        # Create prompt
        if query:
            prompt = f"Below are documents containing information:\n\n{combined_docs}\n\nBased on these documents, {query}"
        else:
            prompt = f"Below are documents containing information:\n\n{combined_docs}\n\nSummarize the key information from these documents."
        
        # Generate response
        return self.generate_response(prompt)