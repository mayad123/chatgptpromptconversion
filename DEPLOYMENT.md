# Deployment Guide for GitHub Pages

## Quick Setup

1. **Ensure your files are in the `docs/` folder**
   - All HTML, CSS, and JS files should be in `docs/`
   - GitHub Pages can serve from `/docs` folder or root

2. **Push to GitHub**
   ```bash
   git add docs/
   git commit -m "Add web interface for prompt optimizer"
   git push origin main
   ```

3. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click **Settings** tab
   - Scroll down to **Pages** section
   - Under **Source**, select:
     - Branch: `main`
     - Folder: `/docs`
   - Click **Save**

4. **Access your site**
   - Your site will be available at:
     `https://mayad123.github.io/chatgptpromptconversion/`
   - It may take a few minutes to deploy

## Alternative: Deploy from root

If you prefer to deploy from the root folder:

1. Move all files from `docs/` to root
2. In GitHub Pages settings, select:
   - Branch: `main`
   - Folder: `/` (root)

## Testing Locally

Before deploying, test locally:

### Option 1: Simple HTTP Server (Python)
```bash
cd docs
python -m http.server 8000
```
Visit: http://localhost:8000

### Option 2: Node.js HTTP Server
```bash
npx http-server docs -p 8000
```
Visit: http://localhost:8000

### Option 3: VS Code Live Server
- Install "Live Server" extension
- Right-click `index.html` > "Open with Live Server"

## Troubleshooting

**Issue:** Site shows 404
- **Solution:** Make sure `/docs` folder is selected in GitHub Pages settings

**Issue:** Changes not showing
- **Solution:** Wait a few minutes, GitHub Pages can take 1-5 minutes to update. Clear browser cache.

**Issue:** JavaScript not working
- **Solution:** Check browser console for errors. Ensure all JS files are in `docs/` folder and paths are correct.

**Issue:** CSS not loading
- **Solution:** Check that `style.css` is in `docs/` folder and the path in `index.html` is correct (`href="style.css"`)

## Custom Domain (Optional)

To use a custom domain:

1. Add a `CNAME` file in `docs/` with your domain:
   ```
   yourdomain.com
   ```
2. Configure DNS with your domain provider
3. Update GitHub Pages settings

## Files Checklist

Ensure these files exist in `docs/`:
- ✅ `index.html`
- ✅ `style.css`
- ✅ `app.js`
- ✅ `prompt-optimizer.js`
- ✅ `README.md` (optional)

