const fs = require('fs');

// Function to record user name and time
function recordUser(username) {
  // Read existing data from the JSON file
  const jsonData = require('./data.json');

  // Get the current time
  const currentTime = new Date();

  // Add user name and time to the JSON object
  jsonData[username] = currentTime;

  // Convert the modified data back to JSON format
  const updatedData = JSON.stringify(jsonData, null, 2);

  // Write the updated data to the JSON file
  fs.writeFileSync('./data.json', updatedData);

  console.log(`Recorded user '${username}' with time '${currentTime}'.`);
}

// Function to remove user name and time
function removeUser(username) {
  // Read existing data from the JSON file
  const jsonData = require('./data.json');

  // Remove the user entry from the JSON object
  delete jsonData[username];

  // Convert the modified data back to JSON format
  const updatedData = JSON.stringify(jsonData, null, 2);

  // Write the updated data to the JSON file
  fs.writeFileSync('./data.json', updatedData);

  console.log(`Removed user '${username}' from the record.`);

  
}
module.exports = {
    recordUser,
    removeUser
};

