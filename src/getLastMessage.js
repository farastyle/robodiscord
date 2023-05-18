const updateMessage = async (channel, text) => {
    let lastMessageId = channel.lastMessageId;
    if (!lastMessageId) {
      // Send the initial message if the last bot-generated message ID is not stored
      const message = await channel.send({ content: text });
      channel.lastMessageId = message.id;
    } else {
      let lastMessage = await channel.messages.fetch(lastMessageId);
      await lastMessage.edit({ content: text });
    }
  };
  
  module.exports = { updateMessage };
  