require('dotenv').config();
const { recordUser, removeUser } = require('./jsoncontrol');
const { SlashCommandBuilder } = require('@discordjs/builders');
const { Client, GatewayIntentBits, Partials, ButtonBuilder, ActionRowBuilder } = require('discord.js');
const { getLastMessage } = require('./getLastMessage');

const client = new Client({ intents: [GatewayIntentBits.Guilds], partials: [Partials.Channel] });

const token = process.env.DISCORD_API_TOKEN;

let texto1 = [];
let texto2 = [];
let channelName = "mecsbot";

const enterButton = new ButtonBuilder()
  .setCustomId('enter')
  .setLabel('Entrar')
  .setStyle('1');

const leaveButton = new ButtonBuilder()
  .setCustomId('leave')
  .setLabel('Sair')
  .setStyle('4');

const butoes = new ActionRowBuilder()
  .addComponents(enterButton, leaveButton);

let lastMessageId; // Store the ID of the last bot-generated message

let jsonData = require('./data.json');
let users = Object.keys(jsonData);
let text1 = texto1.length > 0 ? texto1.join('\n') : 'Ninguém';
let text2 = texto2.length > 0 ? texto2.join('\n') : 'Nenhum registro ainda';
let text = "```**Quem está trabalhando :**\n" + text1 + "\n**Log de chegada e saída:**\n" +  text2 + "```";
client.on('ready', async () => {
  console.log('O bot está online!');
  const lastMessage = await getLastMessage(channelName);
  lastMessageId = lastMessage ? lastMessage.id : null;
  

  // Update the texto1 array with user information from the JSON file
  texto1 = users.map(username => `${username} - ${jsonData[username]}`);

  text1 = texto1.length > 0 ? texto1.join('\n') : 'Ninguém';
  text2 = texto2.length > 0 ? texto2.join('\n') : 'Nenhum registro ainda';
  text = "```**Quem está trabalhando :**\n" + text1 + "\n**Log de chegada e saída:**\n" +  text2 + "```";

  client.channels.cache.forEach(async channel => {
    if (channel.name === channelName) {
      channel.send({ content: 'Controle de Mecs:', components: [butoes]});
      const message2 = await channel.send({ content: text });
      console.log('ID da msg ' + message2.id);
      channel.lastMessageId = message2.id; // Store the last message ID in the channel object
    }
  });
});

client.on('interactionCreate', async (interaction) => {
  
  let channelId = interaction.channelId;
  let channel = client.channels.fetch(channelId);
  jsonData = require('./data.json');
  users = Object.keys(jsonData);
  // Update the texto1 array with user information from the JSON file
  const user = interaction.user.username;
  const time = new Date().toLocaleTimeString();
  texto1 = users.map(username => `${username} - ${jsonData[username]}`);
  console.log('Interaction test!');
  if (!interaction.isButton()) return;

  if (interaction.customId === 'enter') {
    recordUser(user);
    texto1 = users.map(username => `${username} - ${jsonData[username]}`);
  }

  if (interaction.customId === 'leave') {
    removeUser(user);
    texto1 = users.map(username => `${username} - ${jsonData[username]}`);
  }
  
  text1 = texto1.length > 0 ? texto1.join('\n') : 'Ninguém';
  text2 = texto2.length > 0 ? texto2.join('\n') : 'Nenhum registro ainda';
  text = "``` Quem está trabalhando  : **\n" + text1 + "\n\n\n\n\n**Log de chegada e saída:**\n" +  text2 + "```";

  if (!lastMessageId) {
    // Send the initial message if the last bot-generated message ID is not stored
    Console.log('this one' );
    message = channel.send({ content: text });
    
  } else {
    let lastMessage = await channel.messages.fetch(lastMessageId);
    Console.log(' start ' + lastMessage + ' end' );
    await lastMessage.edit({ content: text });
  }
});

client.login(token);
