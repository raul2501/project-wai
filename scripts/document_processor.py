"""
Document processor for Wai.
Combines functionality to extract content from multiple document sources:
- Google Docs
- Google Sheets
- Notion
"""

import os
import sys
import argparse
from typing import Dict, List, Any, Optional, Union

# Add the parent directory to the path so we can import from config and other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Notion and Google Workspace functionality
from scripts.notion_test import get_notion_client, get_page_content, search_notion
from scripts.google_workspace import GoogleWorkspace

# Import configurations
from config.notion_config import DEFAULT_PAGE_ID
from config.google_workspace_config import (
    SAMPLE_DOCUMENT_ID,
    SAMPLE_SPREADSHEET_ID,
    DEFAULT_SHEET_RANGE
)


def extract_from_notion(page_id: str = DEFAULT_PAGE_ID) -> str:
    """Extract content from Notion page."""
    print(f"Extracting content from Notion page: {page_id}")
    content = get_page_content(page_id)
    return content


def extract_from_google_doc(doc_id: str) -> str:
    """Extract content from Google Doc."""
    print(f"Extracting content from Google Doc: {doc_id}")
    client = GoogleWorkspace()
    content = client.read_document(doc_id)
    return content


def extract_from_google_sheet(sheet_id: str, range_name: str = None) -> List[List[Any]]:
    """Extract data from Google Sheet."""
    if range_name is None:
        range_name = DEFAULT_SHEET_RANGE
    print(f"Extracting data from Google Sheet: {sheet_id}, range: {range_name}")
    client = GoogleWorkspace()
    data = client.read_spreadsheet(sheet_id, range_name)
    return data


def process_document(source: str, doc_id: str, **kwargs) -> Any:
    """
    Process document from specified source.
    
    Args:
        source: Document source ('notion', 'gdoc', or 'gsheet')
        doc_id: Document identifier
        **kwargs: Additional source-specific parameters
    
    Returns:
        Document content (string for text documents, list for spreadsheets)
    """
    if source.lower() == 'notion':
        return extract_from_notion(doc_id)
    
    elif source.lower() == 'gdoc':
        return extract_from_google_doc(doc_id)
    
    elif source.lower() == 'gsheet':
        range_name = kwargs.get('range', DEFAULT_SHEET_RANGE)
        return extract_from_google_sheet(doc_id, range_name)
    
    else:
        raise ValueError(f"Unsupported document source: {source}")


def format_preview(content: Any) -> str:
    """Format content preview based on content type."""
    if isinstance(content, str):
        # Text content preview
        preview = content[:500]
        if len(content) > 500:
            preview += "..."
        return f"\nContent preview:\n{preview}\n\nTotal length: {len(content)} characters"
    
    elif isinstance(content, list):
        # Table data preview
        preview = "\nData preview:\n"
        for i, row in enumerate(content[:5]):
            preview += f"Row {i+1}: {row}\n"
        if len(content) > 5:
            preview += f"... and {len(content) - 5} more rows"
        return preview
    
    else:
        return "Content type not supported for preview"


def main():
    """Main entry point for the document processor."""
    parser = argparse.ArgumentParser(description='Process documents from various sources')
    parser.add_argument('--source', choices=['notion', 'gdoc', 'gsheet'], required=True,
                      help='Document source (notion, gdoc, gsheet)')
    parser.add_argument('--id', help='Document ID')
    parser.add_argument('--range', help='Sheet range for Google Sheets (e.g. "A1:Z100")')
    parser.add_argument('--output', help='Output file path (optional)')
    args = parser.parse_args()
    
    # Get document ID, with defaults for each source
    doc_id = args.id
    if not doc_id:
        if args.source == 'notion':
            doc_id = DEFAULT_PAGE_ID
        elif args.source == 'gdoc':
            doc_id = SAMPLE_DOCUMENT_ID
        elif args.source == 'gsheet':
            doc_id = SAMPLE_SPREADSHEET_ID
    
    if not doc_id or doc_id == "YOUR_DOCUMENT_ID":
        print(f"Error: No document ID provided for {args.source}")
        print("Please specify with --id parameter")
        return
    
    # Process the document
    try:
        content = process_document(args.source, doc_id, range=args.range)
        
        # Save to output file if specified
        if args.output and content:
            with open(args.output, 'w') as f:
                if isinstance(content, str):
                    f.write(content)
                elif isinstance(content, list):
                    for row in content:
                        f.write(str(row) + '\n')
            print(f"Content saved to {args.output}")
        
        # Print preview
        print(format_preview(content))
        
    except Exception as e:
        print(f"Error processing document: {e}")


if __name__ == "__main__":
    main()