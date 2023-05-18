require('dotenv').config();
const { recordUser, removeUser } = require('./src/jsoncontrol');
const { SlashCommandBuilder } = require('@discordjs/builders');
const { Client, GatewayIntentBits, Partials, ButtonBuilder, ActionRowBuilder } = require('discord.js');
const { updateMessage } = require('./src/getLastMessage'); // Updated import path

const token = process.env.DISCORD_API_TOKEN;

let texto1 = [];
let texto2 = [];
const channelName = "mecsbot";

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

let jsonData = require('./src/data.json'); // Updated import path
let users = Object.keys(jsonData);
let text1 = texto1.length > 0 ? texto1.join('\n') : 'Ninguém';
let text2 = texto2.length > 0 ? texto2.join('\n') : 'Nenhum registro ainda';
let text = "```**Quem está trabalhando :**\n" + text1 + "\n**Log de chegada e saída:**\n" +  text2 + "```";

const client = new Client({ intents: [GatewayIntentBits.Guilds], partials: [Partials.Channel] });

client.on('ready', async () => {
  console.log('O bot está online!');

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
  let channel = await client.channels.fetch(channelId);
  channel = channel.isText() ? channel : await channel.fetch();
  jsonData = require('./src/data.json'); // Updated import path
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

  updateMessage(channel, text);
});

client.login(token);
