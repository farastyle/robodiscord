require('dotenv').config();
const { SlashCommandBuilder } = require('@discordjs/builders');
const { Client, GatewayIntentBits, Partials, ButtonBuilder, ActionRowBuilder } = require('discord.js');

const client = new Client({ intents: [GatewayIntentBits.Guilds], partials: [Partials.Channel] });

// const { Client, ButtonBuilder, ButtonStyle, SlashCommandBuilder  } = require('discord.js');



const token = process.env.DISCORD_API_TOKEN;

let texto1 = [];
let texto2 = [];
const channelName = "mecs2";

const enterButton = new ButtonBuilder()
  .setCustomId('enter')
  .setLabel('Entrar')
  .setStyle('1');

const leaveButton = new ButtonBuilder()
  .setCustomId('leave')
  .setLabel('Sair')
  .setStyle('4');

const row = new ActionRowBuilder()
  .addComponents(enterButton, leaveButton);

client.on('ready', () => {
  console.log('O bot está online!');

  client.channels.cache.forEach(channel => {
    texto1 = texto1.length > 0 ? texto1.join('\n') : 'Ninguém';
    texto2 = texto2.length > 0 ? texto2.join('\n') : 'Nenhum registro ainda';
    text = "```**Quem está trabalhando:**\n${texto1 || 'Ninguém'}\n\n**Log de chegada e saída:**\n${texto2 || 'Nenhum registro ainda'}```"


    if (channel.name === channelName) {
      channel.send({ content: 'Controle de Mecs:', components: [row], text});

    }
  });
});

client.on('interactionCreate', async interaction => {
  if (!interaction.isButton()) return;

  const user = interaction.user.username;
  const time = new Date().toLocaleTimeString();

  if (interaction.customId === 'enter') {
    texto1.push(`${user} - ${time}`);
    texto2.push(`${user} entrou às ${time}`);
  }

  if (interaction.customId === 'leave') {
    const index = texto1.indexOf(`${user} - ${time}`);
    if (index > -1) {
      texto1.splice(index, 1);
      texto2.push(`${user} saiu às ${time}`);
    }
  }

  const messages = await interaction.channel.messages.fetch();
  const lastMessage = messages.last();

  lastMessage.edit(`Texto 1:\n${texto1.join('\n')}`);
  lastMessage.channel.send(`Texto 2:\n${texto2.join('\n')}`);
});

client.login(token);
