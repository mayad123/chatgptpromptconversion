// Initialize the prompt optimizer
const optimizer = new PromptOptimizer();

// DOM elements
const inputTextarea = document.getElementById('naturalLanguageInput');
const optimizeBtn = document.getElementById('optimizeBtn');
const resultSection = document.getElementById('resultSection');
const responseSection = document.getElementById('responseSection');
const loadingSection = document.getElementById('loadingSection');
const loadingText = document.getElementById('loadingText');
const optimizedOutput = document.getElementById('optimizedOutput');
const chatGptResponse = document.getElementById('chatGptResponse');
const copyBtn = document.getElementById('copyBtn');
const copyToChatGPTBtn = document.getElementById('copyToChatGPTBtn');
const copyResponseBtn = document.getElementById('copyResponseBtn');
const getResponseBtn = document.getElementById('getResponseBtn');
const resetBtn = document.getElementById('resetBtn');
const apiKeyInput = document.getElementById('apiKeyInput');
const saveApiKeyBtn = document.getElementById('saveApiKeyBtn');
const apiKeyStatus = document.getElementById('apiKeyStatus');

// Event listeners
optimizeBtn.addEventListener('click', handleOptimize);
copyBtn.addEventListener('click', handleCopy);
copyToChatGPTBtn.addEventListener('click', handleCopyToChatGPT);
copyResponseBtn.addEventListener('click', handleCopyResponse);
getResponseBtn.addEventListener('click', handleGetResponse);
resetBtn.addEventListener('click', handleReset);
saveApiKeyBtn.addEventListener('click', handleSaveApiKey);

// Load API key from localStorage on page load
window.addEventListener('DOMContentLoaded', () => {
    const savedApiKey = localStorage.getItem('openai_api_key');
    if (savedApiKey) {
        apiKeyInput.value = savedApiKey;
        apiKeyStatus.textContent = '✓ Saved';
        apiKeyStatus.className = 'api-key-status';
    }
});

// Allow Enter key to optimize (Ctrl+Enter)
inputTextarea.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        handleOptimize();
    }
});

function handleOptimize() {
    const input = inputTextarea.value.trim();
    
    if (!input) {
        showToast('Please enter some text to optimize', 'error');
        return;
    }
    
    // Show loading
    loadingSection.style.display = 'block';
    resultSection.style.display = 'none';
    
    // Simulate slight delay for better UX
    setTimeout(() => {
        try {
            const optimized = optimizer.optimize(input);
            
            // Display result
            optimizedOutput.textContent = optimized;
            resultSection.style.display = 'block';
            loadingSection.style.display = 'none';
            
            // Scroll to result
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } catch (error) {
            console.error('Error optimizing prompt:', error);
            showToast('An error occurred while optimizing. Please try again.', 'error');
            loadingSection.style.display = 'none';
        }
    }, 300);
}

function handleCopy() {
    const text = optimizedOutput.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showToast('✅ Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy. Please select and copy manually.', 'error');
    });
}

function handleCopyToChatGPT() {
    const text = optimizedOutput.textContent;
    
    // Copy to clipboard first
    navigator.clipboard.writeText(text).then(() => {
        // Open ChatGPT in a new tab
        window.open('https://chat.openai.com', '_blank');
        showToast('✅ Prompt copied! Opening ChatGPT...', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy. Please copy manually.', 'error');
    });
}

function handleReset() {
    inputTextarea.value = '';
    resultSection.style.display = 'none';
    responseSection.style.display = 'none';
    chatGptResponse.textContent = '';
    inputTextarea.focus();
}

function handleSaveApiKey() {
    const apiKey = apiKeyInput.value.trim();
    
    if (!apiKey) {
        apiKeyStatus.textContent = 'Please enter an API key';
        apiKeyStatus.className = 'api-key-status error';
        return;
    }
    
    if (!apiKey.startsWith('sk-')) {
        apiKeyStatus.textContent = 'Invalid API key format';
        apiKeyStatus.className = 'api-key-status error';
        return;
    }
    
    localStorage.setItem('openai_api_key', apiKey);
    apiKeyStatus.textContent = '✓ Saved';
    apiKeyStatus.className = 'api-key-status';
    showToast('API key saved!', 'success');
}

async function handleGetResponse() {
    const optimizedPrompt = optimizedOutput.textContent;
    
    if (!optimizedPrompt) {
        showToast('Please optimize a prompt first', 'error');
        return;
    }
    
    const apiKey = apiKeyInput.value.trim() || localStorage.getItem('openai_api_key');
    
    if (!apiKey) {
        showToast('Please enter your OpenAI API key', 'error');
        apiKeyInput.focus();
        return;
    }
    
    if (!apiKey.startsWith('sk-')) {
        showToast('Invalid API key format. API keys should start with "sk-"', 'error');
        return;
    }
    
    // Show loading
    loadingSection.style.display = 'block';
    loadingText.textContent = 'Getting response from ChatGPT...';
    responseSection.style.display = 'none';
    
    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [
                    {
                        role: 'user',
                        content: optimizedPrompt
                    }
                ],
                temperature: 0.7,
                max_tokens: 2000
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error?.message || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const chatResponse = data.choices[0].message.content;
        
        // Display response with markdown-like formatting
        chatGptResponse.textContent = chatResponse;
        
        responseSection.style.display = 'block';
        loadingSection.style.display = 'none';
        
        // Scroll to response
        responseSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        console.error('Error getting response:', error);
        
        let errorMessage = 'Failed to get response from ChatGPT. ';
        
        // Check for CORS errors
        if (error.message.includes('CORS') || error.message.includes('Failed to fetch') || 
            error.message.includes('network') || error.message === 'TypeError: Failed to fetch') {
            errorMessage = '⚠️ CORS Error: Browser blocked the request. ';
            errorMessage += 'To fix this, you can:\n';
            errorMessage += '1. Use a CORS browser extension\n';
            errorMessage += '2. Run a local proxy server\n';
            errorMessage += '3. Use the "Open in ChatGPT" button instead';
            
            // Show a more detailed message in the response box
            chatGptResponse.textContent = errorMessage + '\n\nFor developers: OpenAI API requires server-side requests or CORS proxy.';
            responseSection.style.display = 'block';
        } else if (error.message.includes('401') || error.message.includes('Incorrect API key')) {
            errorMessage += 'Invalid API key. Please check your API key.';
        } else if (error.message.includes('429')) {
            errorMessage += 'Rate limit exceeded. Please try again later.';
        } else if (error.message.includes('quota')) {
            errorMessage += 'API quota exceeded. Please check your OpenAI account.';
        } else {
            errorMessage += error.message || 'Please try again.';
        }
        
        showToast(errorMessage, 'error');
        loadingSection.style.display = 'none';
    }
}

function handleCopyResponse() {
    const text = chatGptResponse.textContent;
    
    if (!text) {
        showToast('No response to copy', 'error');
        return;
    }
    
    navigator.clipboard.writeText(text).then(() => {
        showToast('✅ Response copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy. Please select and copy manually.', 'error');
    });
}

function showToast(message, type = 'success') {
    // Remove existing toast if any
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.background = type === 'error' ? '#e74c3c' : '#27ae60';
    
    document.body.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

