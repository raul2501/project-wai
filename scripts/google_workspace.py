"""
Google Workspace integration for Wai.
Provides functionality to access and extract data from Google Docs and Sheets.
"""
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import Dict, List, Any, Optional, Union
import sys

# Add the parent directory to the path so we can import from config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.google_workspace_config import (
    SCOPES,
    DEFAULT_SHEET_RANGE,
    SAMPLE_DOCUMENT_ID,
    SAMPLE_SPREADSHEET_ID
)

# Path to configuration files
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
TOKEN_PATH = os.path.join(CONFIG_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(CONFIG_DIR, 'credentials.json')


def get_credentials():
    """
    Get and refresh credentials for Google API access.
    Returns authenticated credentials object.
    """
    creds = None
    
    # Create config directory if it doesn't exist
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    # Load existing credentials if available
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"Google API credentials not found at {CREDENTIALS_PATH}. "
                    "Please download credentials.json from Google Cloud Console "
                    "and place it in the config directory."
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


class GoogleWorkspace:
    """Client for interacting with Google Workspace APIs."""
    
    def __init__(self):
        """Initialize services for Google Docs and Sheets."""
        self.credentials = get_credentials()
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
    
    def read_document(self, document_id: str) -> str:
        """
        Read content from a Google Doc.
        
        Args:
            document_id: The ID of the document to read
            
        Returns:
            String containing the document's text content
        """
        try:
            # Get the document content
            document = self.docs_service.documents().get(documentId=document_id).execute()
            
            # Extract text from the document
            doc_content = document.get('body', {}).get('content', [])
            text_content = []
            
            # Process the document structure to extract text
            for element in doc_content:
                if 'paragraph' in element:
                    for para_element in element['paragraph']['elements']:
                        if 'textRun' in para_element:
                            text_content.append(para_element['textRun']['content'])
            
            return ''.join(text_content)
        
        except Exception as e:
            print(f"Error reading Google Doc: {e}")
            return ""
    
    def read_spreadsheet(self, spreadsheet_id: str, range_name: str = DEFAULT_SHEET_RANGE) -> List[List[Any]]:
        """
        Read data from a Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet to read
            range_name: The A1 notation of the range to read
            
        Returns:
            2D list containing the spreadsheet data
        """
        try:
            # Get the spreadsheet content for the specified range
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name).execute()
            
            # Extract and return the values
            values = result.get('values', [])
            return values
        
        except Exception as e:
            print(f"Error reading Google Sheet: {e}")
            return []


if __name__ == "__main__":
    import argparse
    
    # Setup command-line arguments
    parser = argparse.ArgumentParser(description='Google Workspace document reader')
    parser.add_argument('--doc', help='Google Doc ID to read')
    parser.add_argument('--sheet', help='Google Sheet ID to read')
    parser.add_argument('--range', help='Sheet range (e.g. "A1:Z100")', default=DEFAULT_SHEET_RANGE)
    args = parser.parse_args()
    
    # Initialize client
    client = GoogleWorkspace()
    
    # Use command-line args or config values
    document_id = args.doc or SAMPLE_DOCUMENT_ID
    spreadsheet_id = args.sheet or SAMPLE_SPREADSHEET_ID
    
    # Check if we should read a document
    if document_id and document_id != "YOUR_DOCUMENT_ID":
        print(f"Reading Google Doc: {document_id}")
        doc_content = client.read_document(document_id)
        if doc_content:
            # Print first 500 chars with a preview indicator
            preview = doc_content[:500]
            if len(doc_content) > 500:
                preview += "..."
            print(f"\nDocument content preview:\n{preview}\n")
            print(f"Total document length: {len(doc_content)} characters")
        else:
            print("No content found or error occurred.")
    
    # Check if we should read a spreadsheet
    if spreadsheet_id and spreadsheet_id != "YOUR_SPREADSHEET_ID":
        print(f"\nReading Google Sheet: {spreadsheet_id}")
        sheet_range = args.range
        sheet_data = client.read_spreadsheet(spreadsheet_id, sheet_range)
        if sheet_data:
            # Print first 5 rows
            print(f"\nSpreadsheet data preview (range {sheet_range}):")
            for i, row in enumerate(sheet_data[:5]):
                print(f"Row {i+1}: {row}")
            if len(sheet_data) > 5:
                print(f"... and {len(sheet_data) - 5} more rows")
        else:
            print("No data found or error occurred.")
    
    # If no valid IDs provided, show usage message
    if ((not document_id or document_id == "YOUR_DOCUMENT_ID") and 
        (not spreadsheet_id or spreadsheet_id == "YOUR_SPREADSHEET_ID")):
        print("\nUsage examples:")
        print("  python google_workspace.py --doc=YOUR_DOCUMENT_ID")
        print("  python google_workspace.py --sheet=YOUR_SPREADSHEET_ID")
        print("  python google_workspace.py --doc=YOUR_DOCUMENT_ID --sheet=YOUR_SPREADSHEET_ID")
        print("\nUpdate SAMPLE_DOCUMENT_ID and SAMPLE_SPREADSHEET_ID in config/google_workspace_config.py")
        print("or provide IDs via command-line arguments.")