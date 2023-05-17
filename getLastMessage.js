const { Client, Intents } = require('discord.js');
const channelName = 'mecsbot';  // // Set your default channel ID here
const defaultLastMessageId = '1108528121185046618'; // Set your default message ID here

client.on('ready', async () => {
  console.log('O bot está online!');

  const channel = client.channels.cache.find(channel => channel.name === channelName);
  if (!channel) {
    console.error(`Channel '${channelName}' not found.`);
    return;
  }

  let lastMessageId;
  const lastMessage = await getLastMessage(channel);
  if (lastMessage) {
    console.log('Found last message:', lastMessage.content);
    lastMessageId = lastMessage.id; // Store the ID of the last message
  } else if (defaultLastMessageId) {
    console.log('Using default last message ID:', defaultLastMessageId);
    lastMessageId = defaultLastMessageId; // Use the default message ID
  } else {
    console.error('No last message found.');
    return;
  }

  // Export the last message ID
  console.log('Exporting last message ID:', lastMessageId);
  module.exports.lastMessageId = lastMessageId;

  client.destroy();
});

async function getLastMessage(channel) {
  try {
    const messages = await channel.messages.fetch({ limit: 1 });
    return messages.first();
  } catch (error) {
    console.error('Error retrieving last message:', error);
    return null;
  }
}

client.login(process.env.DISCORD_API_TOKEN);
