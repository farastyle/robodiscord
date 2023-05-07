import os
from dotenv import load_dotenv
import discord
from discord import Button, ButtonStyle
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('HIDDEN')
GUILD = os.getenv('TESTE')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

async def create_button_row(activities):
    buttons_row1 = [Button(style=ButtonStyle.green, label="Logar", custom_id="logar_button")]
    row1 = activities[0:5]
    row2 = activities[5:10]

    for activity in row1:
        button = Button(style=ButtonStyle.blue, label=activity, custom_id=activity.lower().replace(" ", "_"))
        buttons_row1.append(button)

    buttons_row2 = []

    for activity in row2:
        button = Button(style=ButtonStyle.blue, label=activity, custom_id=activity.lower().replace(" ", "_"))
        buttons_row2.append(button)

    return [buttons_row1, buttons_row2]

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    channel = discord.utils.get(guild.channels, name='controle-mecanica')
    if channel is None:
        print("Channel not found")
        return

    message = await channel.send("Controle de atividades da Mecanica:", components=await create_button_row(set()))
    print(f'Message sent: {message.content}')

@bot.event
async def on_button_click(interaction):
    await interaction.respond(type=6)

bot.run(TOKEN)
