Wai - AI-Powered Document Assistant

Wai is an AI-powered document assistant that integrates with Notion and Google Workspace to provide intelligent insights and responses to your documents.

FEATURES

- Multiple Document Sources: Integrate with Notion, Google Docs, and Google Sheets
- AI-Powered Analysis: Use Llama-3 to understand and respond to your documents
- Simple Web Interface: Ask questions about your documents with an easy-to-use web UI

ARCHITECTURE

- Frontend: HTML/CSS/JavaScript web application
- Backend: FastAPI Python server
- AI Engine: Llama-3 model integration
- Data Sources: Notion API, Google Workspace API

SETUP AND INSTALLATION

Prerequisites:
- Python 3.8+
- Node.js and npm (for frontend development)
- Notion API key
- Google API credentials

Installation:

1. Clone the repository
   git clone https://github.com/yourusername/wai.git
   cd wai

2. Install Python dependencies
   pip install -r requirements.txt

3. Set up configuration files
   - Copy your Notion API key to config/notion_config.py
   - Place your Google API credentials in config/credentials.json

4. Run the backend server
   python backend/server.py

5. Serve the frontend
   During development, you can use any static file server:
   cd frontend
   python -m http.server 3000

   Or for more advanced development, set up a Node.js development server.

USAGE

1. Open the web interface in your browser (default: http://localhost:3000)
2. Select your document source (Notion, Google Docs, or Google Sheets)
3. Enter the document ID
4. Ask a question about your document
5. View the AI-generated response

DEVELOPMENT

Project Structure:
wai/
   backend/             # Backend server code
      ai/              # AI model integration
      api/             # API endpoints
      server.py        # FastAPI server
   config/              # Configuration files
   docs/                # Documentation
   frontend/            # Web frontend
      src/             # Source files
   scripts/             # Utility scripts
      document_processor.py
      google_workspace.py
      notion_test.py
   tests/               # Test suite

Running Tests:
pytest tests/

CONTRIBUTING

Contributions are welcome! Please feel free to submit a Pull Request.