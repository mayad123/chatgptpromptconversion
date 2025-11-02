// Initialize the prompt optimizer
const optimizer = new PromptOptimizer();

// DOM elements
const inputTextarea = document.getElementById('naturalLanguageInput');
const optimizeBtn = document.getElementById('optimizeBtn');
const resultSection = document.getElementById('resultSection');
const loadingSection = document.getElementById('loadingSection');
const optimizedOutput = document.getElementById('optimizedOutput');
const copyBtn = document.getElementById('copyBtn');
const copyToChatGPTBtn = document.getElementById('copyToChatGPTBtn');
const resetBtn = document.getElementById('resetBtn');

// Event listeners
optimizeBtn.addEventListener('click', handleOptimize);
copyBtn.addEventListener('click', handleCopy);
copyToChatGPTBtn.addEventListener('click', handleCopyToChatGPT);
resetBtn.addEventListener('click', handleReset);

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
    
    if (!text) {
        showToast('Please optimize a prompt first', 'error');
        return;
    }
    
    // Copy to clipboard first - ensure it works
    if (navigator.clipboard && navigator.clipboard.writeText) {
        // Modern clipboard API
        navigator.clipboard.writeText(text).then(() => {
            // Small delay to ensure clipboard is ready
            setTimeout(() => {
                // Open ChatGPT in a new tab
                window.open('https://chat.openai.com', '_blank');
                showToast('✅ Prompt copied to clipboard! Opening ChatGPT...', 'success');
            }, 150);
        }).catch(err => {
            console.error('Failed to copy:', err);
            // Fallback: try old method
            fallbackCopyTextToClipboard(text);
        });
    } else {
        // Fallback for older browsers
        fallbackCopyTextToClipboard(text);
    }
}

// Fallback copy method for browsers without clipboard API
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            setTimeout(() => {
                window.open('https://chat.openai.com', '_blank');
                showToast('✅ Prompt copied to clipboard! Opening ChatGPT...', 'success');
            }, 150);
        } else {
            showToast('Copy failed. Please use the Copy button, then open ChatGPT manually.', 'error');
        }
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showToast('Copy failed. Please use the Copy button, then open ChatGPT manually.', 'error');
    } finally {
        document.body.removeChild(textArea);
    }
}

function handleReset() {
    inputTextarea.value = '';
    resultSection.style.display = 'none';
    inputTextarea.focus();
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

