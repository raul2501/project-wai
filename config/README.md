# Configuration Files

This directory contains configuration files for the Wai project.

## Notion API Configuration

- `notion_config.py` - Contains Notion API token and settings

## Google Workspace Configuration

### Required Files:
- `google_workspace_config.py` - General configuration settings
- `credentials.json` - OAuth 2.0 credentials file downloaded from Google Cloud Console
  - Copy `credentials.example.json` to `credentials.json` and add your credentials
  - **IMPORTANT: Never commit real credentials to the repository!**
- `token.pickle` - Authentication token (auto-generated after first authentication)

### How to set up Google Workspace API access:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Docs API and Google Sheets API
4. Go to "Credentials" and create an OAuth 2.0 Client ID
5. Download the credentials as JSON and save to `config/credentials.json` (or use the example template)
6. Run the Google Workspace script once to authenticate and generate the token

**Note: You need to create new credentials as the previous ones were exposed in git history.**