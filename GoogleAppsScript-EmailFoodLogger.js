// Google Apps Script - Email Food Logger
// Monitors Gmail for FOOD emails and logs to Google Sheets
// No credentials needed - runs in YOUR Google account!

function checkFoodEmails() {
  const SHEET_ID = '1LYz3qgsR5GF3tt-ut6PpOVyKfCb4y-H6a5EW8Okw5SI';
  const SEARCH_QUERY = 'subject:FOOD is:unread';

  // Get Google Sheet
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName("Meals");

  // Add headers if sheet is empty
  if (sheet.getLastRow() === 0) {
    sheet.appendRow([
      "Timestamp", "Food", "Portion", "Calories", "Protein (g)",
      "Carbs (g)", "Fat (g)", "Meal Type", "Source", "Confidence"
    ]);
  }

  // Search for unread FOOD emails
  const threads = GmailApp.search(SEARCH_QUERY);

  threads.forEach(thread => {
    const messages = thread.getMessages();

    messages.forEach(message => {
      if (message.isUnread()) {
        // Get email content
        const body = message.getPlainBody();
        const subject = message.getSubject();
        const attachments = message.getAttachments();

        // Save images to Google Drive
        let imageInfo = [];
        attachments.forEach(attachment => {
          if (attachment.getContentType().startsWith("image/")) {
            const file = DriveApp.createFile(attachment);
            imageInfo.push({
              url: file.getUrl(),
              name: file.getName()
            });
          }
        });

        // Simple food extraction from email body
        const foods = extractFoodFromText(body);
        const mealType = determineMealType(message.getDate());

        // Log each food item
        const timestamp = Utilities.formatDate(message.getDate(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");

        foods.forEach(food => {
          sheet.appendRow([
            timestamp,
            food.name,
            food.portion_size,
            food.calories,
            food.protein_g,
            food.carbs_g,
            food.fat_g,
            mealType,
            "Email" + (imageInfo.length > 0 ? " (" + imageInfo.length + " images)" : ""),
            imageInfo.length > 0 ? "medium" : "low"
          ]);
        });

        // Mark as read
        message.markRead();
        
        Logger.log("Processed email from: " + message.getFrom() + " with " + foods.length + " food items");
      }
    });
  });
}

function extractFoodFromText(text) {
  // Simple food extraction
  // You can enhance this with Gemini API later!

  const lines = text.split("
");
  const foods = [];

  // Look for food keywords
  const foodKeywords = ["ate", "eating", "had", "meal", "breakfast", "lunch", "dinner", "snack"];

  lines.forEach(line => {
    const lowerLine = line.toLowerCase();
    if (foodKeywords.some(keyword => lowerLine.includes(keyword))) {
      // Extract food name (simple version)
      foods.push({
        name: line.substring(0, 100),
        portion_size: "1 serving",
        calories: 400,  // Estimate - enhance with Gemini API
        protein_g: 20,
        carbs_g: 40,
        fat_g: 15
      });
    }
  });

  // If no foods found, create generic entry
  if (foods.length === 0) {
    foods.push({
      name: text.substring(0, 50) || "Meal",
      portion_size: "1 serving",
      calories: 400,
      protein_g: 20,
      carbs_g: 40,
      fat_g: 15
    });
  }

  return foods;
}

function determineMealType(timestamp) {
  const hour = timestamp.getHours();
  if (hour < 10) return "breakfast";
  if (hour < 14) return "lunch";
  if (hour < 17) return "snack";
  return "dinner";
}

// Run this once to create the trigger
function setupTrigger() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));

  // Create new trigger - runs every 2 minutes
  ScriptApp.newTrigger("checkFoodEmails")
    .timeBased()
    .everyMinutes(2)
    .create();

  Logger.log("Trigger created! Will check emails every 2 minutes.");
}
