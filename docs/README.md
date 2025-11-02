# ChatGPT Prompt Optimizer - Web Interface

This is the web interface for the ChatGPT Prompt Optimization Agent, hosted on GitHub Pages.

## View Live

The site is available at: `https://mayad123.github.io/chatgptpromptconversion/`

## Local Development

To test locally:

1. Open `index.html` in a web browser
2. Or use a local server:
   ```bash
   # Using Python
   cd docs
   python -m http.server 8000
   
   # Using Node.js
   npx http-server docs -p 8000
   ```

Then visit `http://localhost:8000`

## Files Structure

```
docs/
├── index.html          # Main HTML page
├── style.css          # Styling
├── app.js             # Main application logic
├── prompt-optimizer.js # Core optimizer and parser logic
└── README.md          # This file
```

## Features

- ✅ Natural language input processing
- ✅ OpenAI best practices integration
- ✅ Role assignment
- ✅ Context extraction
- ✅ Chain-of-thought for complex tasks
- ✅ Copy to clipboard
- ✅ Direct link to ChatGPT
- ✅ Responsive design
- ✅ No server required (fully client-side)

## Deployment

The site is automatically deployed to GitHub Pages when you push to the `main` branch.

To manually deploy:
1. Ensure all files are in the `docs/` folder
2. Go to GitHub repository Settings > Pages
3. Select source branch and `/docs` folder
4. Save

