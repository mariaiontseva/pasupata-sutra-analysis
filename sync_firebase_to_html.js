// Script to sync Firebase data back to HTML before pushing to GitHub
// Run this before any git push to preserve user's Firebase edits

const admin = require('firebase-admin');
const fs = require('fs');
const { JSDOM } = require('jsdom');

// Initialize Firebase Admin
const serviceAccount = {
  "type": "service_account",
  "project_id": "sanskrit-884a4",
  "private_key_id": "YOUR_PRIVATE_KEY_ID",
  "private_key": "YOUR_PRIVATE_KEY",
  "client_email": "YOUR_CLIENT_EMAIL",
  "client_id": "YOUR_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "YOUR_CERT_URL"
};

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://sanskrit-884a4-default-rtdb.firebaseio.com"
});

const db = admin.database();
const userId = 'pasupata_analysis_shared';

async function syncFirebaseToHtml() {
  try {
    // 1. Read Firebase data
    console.log('📥 Fetching data from Firebase...');
    const snapshot = await db.ref('pasupata_analysis/' + userId).once('value');
    const firebaseData = snapshot.val();

    if (!firebaseData || !firebaseData.data) {
      console.log('⚠️ No Firebase data found');
      return;
    }

    // 2. Read HTML file
    console.log('📄 Reading HTML file...');
    const htmlContent = fs.readFileSync('index.html', 'utf-8');
    const dom = new JSDOM(htmlContent);
    const document = dom.window.document;

    // 3. Update HTML with Firebase data
    console.log('🔄 Syncing Firebase data to HTML...');
    const cellClasses = ['sanskrit', 'words', 'literal', 'translation', 'grammar', 'meaning', 'jims'];
    let totalUpdated = 0;

    cellClasses.forEach(className => {
      if (firebaseData.data[className]) {
        const cells = document.querySelectorAll(`.${className}[contenteditable="true"]`);
        let classUpdated = 0;

        cells.forEach((cell, index) => {
          if (firebaseData.data[className][index]) {
            cell.innerHTML = firebaseData.data[className][index];
            classUpdated++;
            totalUpdated++;
          }
        });

        console.log(`  ✅ ${className}: ${classUpdated} cells updated`);
      }
    });

    // 4. Save updated HTML
    console.log(`💾 Saving updated HTML with ${totalUpdated} cells from Firebase...`);
    fs.writeFileSync('index.html', dom.serialize());

    console.log('✅ Sync complete! HTML now contains latest Firebase data.');
    console.log('You can now safely push to GitHub.');

  } catch (error) {
    console.error('❌ Error syncing:', error);
    process.exit(1);
  } finally {
    process.exit(0);
  }
}

syncFirebaseToHtml();