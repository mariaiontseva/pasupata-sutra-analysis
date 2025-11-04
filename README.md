# Pāśupata Sūtra - Comprehensive Scholarly Analysis

Interactive scholarly translation table for the Pāśupata Sūtra commentary with cloud-based auto-save.

## Features

- ✏️ **Editable Cells**: Both "Word-by-Word Analysis" (blue) and "Literal Translation" (yellow) columns are editable
- ☁️ **Cloud Storage**: Changes automatically sync to Firebase cloud database
- 💾 **Auto-save**: Changes saved 2 seconds after you stop typing
- 🔄 **Cross-Browser Sync**: Open in any browser and see your latest edits
- 🌐 **Real-time Updates**: Changes sync automatically across all open tabs/browsers
- 📝 **5-Column Analysis**:
  - Sanskrit Text
  - Word-by-Word Analysis (editable)
  - Literal Translation (editable)
  - Interpretative Meaning
  - Literary Translation

## How to Use

1. Open the page: https://mariaiontseva.github.io/pasupata-sutra-analysis/
2. Click on any blue (Word-by-Word) or yellow (Literal Translation) cell to edit
3. Type your changes
4. Wait 2 seconds - you'll see "✓ Saved to cloud" notification
5. Open the same page in another browser - your changes will be there!

## Firebase Setup (Required)

The application uses Firebase Realtime Database for cloud storage. To complete the setup:

### Option 1: Using the existing placeholder config (Quick test)
The page currently has placeholder Firebase credentials. For testing purposes:
- The page will load but saving won't work
- You'll see error messages in the browser console

### Option 2: Create your own Firebase project (Recommended)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or "Create a project"
3. Name it "pasupata-sutra-analysis" (or any name you prefer)
4. Follow the setup wizard (disable Google Analytics if not needed)
5. Once created, click "Realtime Database" in the left menu
6. Click "Create Database"
7. Choose a location (e.g., us-central1)
8. Start in **test mode** (we'll configure security later)
9. Click the gear icon → "Project settings"
10. Scroll down to "Your apps" → Click the web icon (`</>`)
11. Register your app with nickname "pasupata-analysis"
12. Copy the `firebaseConfig` object
13. Open `index.html` in your repository
14. Replace the placeholder config (lines 2537-2545) with your real config
15. Commit and push the changes

### Security Rules

After setup, configure Firebase security rules:

1. In Firebase Console → Realtime Database → Rules
2. Replace with:
```json
{
  "rules": {
    "edits": {
      ".read": true,
      ".write": true
    }
  }
}
```

**Note**: This allows anyone to read/write. For private use, you can:
- Keep the database URL private (don't share the GitHub Pages link)
- Add authentication later
- Use more restrictive rules

## Browser Requirements

- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Requires internet connection for cloud sync
- JavaScript must be enabled

## Troubleshooting

### "Save failed" errors
- Check that you've set up Firebase with your own credentials
- Verify the database URL in the config
- Check browser console for specific error messages

### Changes not appearing in other browsers
- Wait a few seconds for sync to complete
- Check that both browsers are using the same Firebase project
- Verify your internet connection

### "No previous edits found"
- This is normal on first use
- Make some edits and they'll be saved for next time

## Technical Details

- **Frontend**: Pure HTML/CSS/JavaScript
- **Database**: Firebase Realtime Database
- **Hosting**: GitHub Pages
- **Auto-save delay**: 2 seconds after last keystroke
- **Real-time sync**: Immediate updates via Firebase listeners

## Academic Use

This tool is designed for dissertation research on the Pāśupata Sūtra, providing an interactive platform for refining translations and grammatical analysis with automatic cloud backup.

## Privacy Note

All edits are stored in your Firebase Realtime Database. With the test mode rules above, anyone with the database URL can read/write data. For sensitive research:
- Keep your Firebase config private
- Don't share your GitHub Pages URL publicly
- Consider adding Firebase Authentication
- Review and tighten security rules
