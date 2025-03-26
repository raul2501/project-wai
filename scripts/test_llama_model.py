"""
Test script for the Llama model integration.
This script allows you to test the model directly with sample inputs.
"""
import os
import sys
import json
import argparse
from typing import List, Optional
import time

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Hugging Face utilities
from huggingface_hub import login

# Import the LlamaModel
from backend.ai.llama_model import LlamaModel


def test_basic_prompt(model: LlamaModel, prompt: str):
    """Test the model with a basic prompt."""
    print("\n=== Testing Basic Prompt ===")
    print(f"Prompt: {prompt}")
    
    # Time the response generation
    start_time = time.time()
    
    # Generate response
    response = model.generate_response(prompt)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    print("\n=== Model Response ===")
    print(response)
    print(f"\nResponse generated in {elapsed_time:.2f} seconds")
    
    return response


def test_document_processing(model: LlamaModel, documents: List[str], query: Optional[str] = None):
    """Test the model's document processing functionality."""
    print("\n=== Testing Document Processing ===")
    print(f"Number of documents: {len(documents)}")
    
    # Print document previews
    for i, doc in enumerate(documents):
        preview = doc[:100] + "..." if len(doc) > 100 else doc
        print(f"\nDocument {i+1} preview: {preview}")
    
    if query:
        print(f"Query: {query}")
    else:
        print("No query provided, model will summarize documents")
    
    # Time the response generation
    start_time = time.time()
    
    # Process documents
    response = model.process_documents(documents, query)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    print("\n=== Model Response ===")
    print(response)
    print(f"\nResponse generated in {elapsed_time:.2f} seconds")
    
    return response


def main():
    """Main function to run the tests."""
    parser = argparse.ArgumentParser(description="Test the Llama model integration")
    parser.add_argument("--model", default="meta-llama/Llama-2-7b-chat-hf", 
                      help="Model name (default: meta-llama/Llama-2-7b-chat-hf)")
    parser.add_argument("--prompt", help="Test a basic prompt")
    parser.add_argument("--document", action="append", help="Add a document for processing (can be used multiple times)")
    parser.add_argument("--doc-file", action="append", help="Path to a document file (can be used multiple times)")
    parser.add_argument("--query", help="Query for document processing")
    parser.add_argument("--save", help="Save responses to a JSON file")
    parser.add_argument("--token", help="Hugging Face token for accessing gated models")
    
    args = parser.parse_args()
    
    # Login to Hugging Face if token is provided
    if args.token:
        print("Logging in to Hugging Face...")
        login(token=args.token)
        print("Login successful!")
    else:
        print("Warning: No Hugging Face token provided. You may not be able to access gated models.")
        print("To access gated models, get a token from https://huggingface.co/settings/tokens")
        print("and pass it using the --token parameter.")
    
    # Initialize the model
    print(f"Initializing Llama model: {args.model}")
    model = LlamaModel(model_name=args.model, token=args.token)
    
    results = {}
    
    # Test with a basic prompt if provided
    if args.prompt:
        results["basic_prompt"] = {
            "prompt": args.prompt,
            "response": test_basic_prompt(model, args.prompt)
        }
    
    # Process documents if provided
    documents = []
    
    # Add documents from command line arguments
    if args.document:
        documents.extend(args.document)
    
    # Add documents from files
    if args.doc_file:
        for file_path in args.doc_file:
            try:
                with open(file_path, 'r') as f:
                    documents.append(f.read())
            except Exception as e:
                print(f"Error reading document file {file_path}: {e}")
    
    if documents:
        results["document_processing"] = {
            "documents": documents,
            "query": args.query,
            "response": test_document_processing(model, documents, args.query)
        }
    
    # Save results if requested
    if args.save and results:
        try:
            with open(args.save, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.save}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    if not args.prompt and not documents:
        print("\nNo tests were run. Please provide at least one of: --prompt, --document, or --doc-file")
        parser.print_help()


if __name__ == "__main__":
    main()