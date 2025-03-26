"""
Configuration file for Google Workspace API integration.
"""

# Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
]

# Default range for spreadsheet data
DEFAULT_SHEET_RANGE = 'A1:Z1000'

# Configuration for API requests
REQUEST_TIMEOUT = 60  # seconds
MAX_RETRY_ATTEMPTS = 3

# Sample document/spreadsheet IDs for testing
# Replace these with actual IDs when ready to test
SAMPLE_DOCUMENT_ID = "YOUR_DOCUMENT_ID"
SAMPLE_SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"