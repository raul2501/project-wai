"""
Configuration file for Slack API integration.
"""

# Slack API token (replace with your actual token)
# You can get this from https://api.slack.com/apps
SLACK_API_TOKEN = "xoxb-your-token-here"

# Default channel ID to access
DEFAULT_CHANNEL_ID = "C0123456789"

# Default time window (in days) for retrieving messages
DEFAULT_TIME_WINDOW = 7

# Maximum number of messages to retrieve per request
MAX_MESSAGES_PER_REQUEST = 100