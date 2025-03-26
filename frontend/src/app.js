// Constants
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const notionBtn = document.getElementById('notion-btn');
const gdocBtn = document.getElementById('gdoc-btn');
const gsheetBtn = document.getElementById('gsheet-btn');
const docIdInput = document.getElementById('doc-id');
const sheetRangeGroup = document.querySelector('.sheet-range-group');
const sheetRangeInput = document.getElementById('sheet-range');
const queryInput = document.getElementById('query');
const processBtn = document.getElementById('process-btn');
const resultsSection = document.querySelector('.results');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');
const aiResponseContent = document.getElementById('ai-response-content');
const documentContentText = document.getElementById('document-content-text');
const loadingSpinner = document.querySelector('.loading-spinner');

// State
let currentSource = 'notion';

// Event Listeners
notionBtn.addEventListener('click', () => setActiveSource('notion'));
gdocBtn.addEventListener('click', () => setActiveSource('gdoc'));
gsheetBtn.addEventListener('click', () => setActiveSource('gsheet'));
processBtn.addEventListener('click', processDocument);

// Tab switching
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.getAttribute('data-tab');
        
        // Update active tab button
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update active tab pane
        tabPanes.forEach(pane => pane.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
    });
});

// Functions
function setActiveSource(source) {
    // Update state
    currentSource = source;
    
    // Update UI
    const sourceButtons = [notionBtn, gdocBtn, gsheetBtn];
    sourceButtons.forEach(btn => btn.classList.remove('active'));
    
    if (source === 'notion') {
        notionBtn.classList.add('active');
        sheetRangeGroup.classList.add('hidden');
        docIdInput.placeholder = 'Enter Notion page ID';
    } else if (source === 'gdoc') {
        gdocBtn.classList.add('active');
        sheetRangeGroup.classList.add('hidden');
        docIdInput.placeholder = 'Enter Google Doc ID';
    } else if (source === 'gsheet') {
        gsheetBtn.classList.add('active');
        sheetRangeGroup.classList.remove('hidden');
        docIdInput.placeholder = 'Enter Google Sheet ID';
    }
}

async function processDocument() {
    // Get input values
    const docId = docIdInput.value.trim();
    const query = queryInput.value.trim();
    const range = sheetRangeInput.value.trim();
    
    // Validate inputs
    if (!docId) {
        alert('Please enter a document ID');
        return;
    }
    
    // Show loading state
    processBtn.disabled = true;
    processBtn.textContent = 'Processing...';
    resultsSection.classList.remove('hidden');
    aiResponseContent.innerHTML = '';
    documentContentText.innerHTML = '';
    loadingSpinner.classList.remove('hidden');
    
    try {
        // Prepare request
        const requestData = {
            source: currentSource,
            doc_id: docId,
            query: query || undefined
        };
        
        // Add range for Google Sheets if provided
        if (currentSource === 'gsheet' && range) {
            requestData.range = range;
        }
        
        // Send API request
        const response = await fetch(`${API_BASE_URL}/documents/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        // Handle response
        if (response.ok) {
            const data = await response.json();
            
            // Display results
            aiResponseContent.textContent = data.ai_response;
            documentContentText.textContent = data.content;
            
            // Ensure the AI response tab is active
            tabBtns.forEach(btn => btn.classList.remove('active'));
            tabBtns[0].classList.add('active');
            tabPanes.forEach(pane => pane.classList.remove('active'));
            tabPanes[0].classList.add('active');
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Something went wrong');
        }
    } catch (error) {
        console.error('Error:', error);
        aiResponseContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    } finally {
        // Reset UI state
        processBtn.disabled = false;
        processBtn.textContent = 'Process Document';
        loadingSpinner.classList.add('hidden');
    }
}

// Initialize
setActiveSource('notion');