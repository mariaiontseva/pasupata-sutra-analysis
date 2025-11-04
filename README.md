# Pāśupata Sūtra - Comprehensive Scholarly Analysis

Interactive scholarly translation table for the Pāśupata Sūtra commentary with cloud-based auto-save.

## Features

- ✏️ **Editable Cells**: Both "Word-by-Word Analysis" (blue) and "Literal Translation" (yellow) columns are editable
- ☁️ **Cloud Storage**: Changes automatically sync to JSONbin cloud database
- 💾 **Auto-save**: Changes saved 2 seconds after you stop typing
- 🔄 **Cross-Browser Sync**: Open in any browser and see your latest edits
- 🔁 **Auto-sync**: Checks for updates from other browsers every 30 seconds
- 💻 **Local Backup**: Always saves to browser localStorage as fallback
- 📝 **5-Column Analysis**:
  - Sanskrit Text
  - Word-by-Word Analysis (editable)
  - Literal Translation (editable)
  - Interpretative Meaning
  - Literary Translation

## Quick Start

1. Open: https://mariaiontseva.github.io/pasupata-sutra-analysis/
2. Click any blue or yellow cell to edit
3. Your changes are automatically saved to your browser

**To sync across browsers:** See setup instructions below.

## Cloud Storage Setup (Optional but Recommended)

The page works immediately with localStorage, but to sync edits across browsers and devices, set up JSONbin (takes 2 minutes):

### Step-by-Step Setup

1. **Create Free JSONbin Account**
   - Go to https://jsonbin.io/
   - Click "Create Account" (free plan is perfect)
   - Verify your email

2. **Get Your API Key**
   - Log in to JSONbin
   - Click "API Keys" tab
   - Copy the API key shown

3. **Update the Config**
   - Open your GitHub repository: `pasupata-sutra-analysis`
   - Edit `index.html`
   - Find line 2537: `const JSONBIN_API_KEY = '$2a$10$zPxQ8vY9wR3kL6mN4tH2sO';`
   - Replace `$2a$10$zPxQ8vY9wR3kL6mN4tH2sO` with your actual API key
   - Commit and push changes

4. **Done!**
   - Refresh the GitHub Pages site
   - The yellow warning banner will disappear
   - Your edits now sync automatically across all browsers!

### What You Get with Cloud Sync

- ✅ Edit on laptop, continue on another device
- ✅ Changes sync automatically every 30 seconds
- ✅ No manual downloading or uploading
- ✅ localStorage still works as backup

### Without Cloud Setup

- ✅ Edits still work perfectly
- ✅ Auto-saves to browser localStorage
- ❌ Won't sync to other browsers/devices
- ⚠️ Yellow warning banner appears

## How to Use

1. **Edit**: Click any blue (Word-by-Word) or yellow (Literal Translation) cell
2. **Type**: Make your changes
3. **Wait**: After 2 seconds of no typing, you'll see "✓ Saved to cloud"
4. **Switch Browser**: Open same URL in another browser - changes are there!

## Browser Requirements

- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Requires internet connection for cloud sync
- JavaScript must be enabled
- Cookies/localStorage enabled

## Troubleshooting

### "Save failed" or "Load failed" errors
- **Check API key**: Make sure you pasted the correct key from JSONbin
- **Check formatting**: The API key should be in quotes, no extra spaces
- **Check internet**: Cloud storage requires internet connection
- **Check browser console**: Press F12, check Console tab for specific errors

### Warning banner won't go away
- **API key not updated**: Make sure you committed and pushed the changes to GitHub
- **Wait for GitHub Pages**: Takes 1-2 minutes to deploy after pushing
- **Hard refresh**: Press Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Changes not appearing in other browsers
- **Wait 30 seconds**: Auto-sync checks every 30 seconds
- **Manual refresh**: Reload the page to force a check
- **Check both browsers**: Both must have internet connection
- **Check API key**: Both browsers must use same GitHub Pages URL with updated config

### "No previous edits found"
- This is normal on first use
- Make some edits and they'll be saved for next time

## Technical Details

- **Frontend**: Pure HTML/CSS/JavaScript
- **Cloud Storage**: JSONbin.io Realtime Database
- **Hosting**: GitHub Pages
- **Auto-save delay**: 2 seconds after last keystroke
- **Sync polling**: Every 30 seconds
- **Local backup**: Immediate save to localStorage on every edit

## Privacy & Security

- **Your data**: Stored in your free JSONbin account
- **API key**: Keep it private - don't share your GitHub repo publicly if configured
- **Public/Private**: By default, JSONbin bins are private (only accessible with your API key)
- **Free tier**: 100K requests/month (more than enough for personal use)

## Academic Use

This tool is designed for dissertation research on the Pāśupata Sūtra, providing an interactive platform for refining translations and grammatical analysis with automatic cloud backup.

## Local Development

To develop and test changes locally before pushing to GitHub:

### Quick Start

```bash
cd /Users/mariaiontseva/pasupata-sutra-analysis
./start-local.sh
```

Then open http://localhost:8080 in your browser.

### Manual Method

```bash
# Start web server
python3 -m http.server 8080

# Open in browser
open http://localhost:8080
```

### Development Workflow

1. Edit `index.html` in your text editor
2. Save the file
3. Refresh browser (Cmd+R) to see changes
4. When ready:
   ```bash
   git add index.html
   git commit -m "Description of changes"
   git push origin master
   ```
5. Wait 1-2 minutes for GitHub Pages to deploy
6. Check https://mariaiontseva.github.io/pasupata-sutra-analysis/

## Files

- `index.html` - Main application with editable table
- `README.md` - This file
- `start-local.sh` - Helper script to start local server
- `.gitignore` - Git ignore rules

## Support

For issues or questions:
- Check the troubleshooting section above
- Check browser console (F12) for error messages
- Verify JSONbin setup at https://jsonbin.io/
