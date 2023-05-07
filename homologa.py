import os
from dotenv import load_dotenv
import discord
from discord import Button, ButtonStyle
from discord.ext import commands
from discord import ButtonStyle



load_dotenv()

TOKEN = 'HIDDEN'
GUILD = 'TESTE'

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

async def create_button_row(activities):
    buttons_row1 = [discord.ui.Button(style=discord.ButtonStyle.green, label="Logar", custom_id="logar_button")]
    row1 = activities[0:5]
    row2 = activities[5:10]

    for activity in row1:
        button = discord.ui.Button(style=discord.ButtonStyle.blue, label=activity, custom_id=activity.lower().replace(" ", "_"))
        buttons_row1.append(button)

    buttons_row2 = []

    for activity in row2:
        button = discord.ui.Button(style=discord.ButtonStyle.blue, label=activity, custom_id=activity.lower().replace(" ", "_"))
        buttons_row2.append(button)

    return [buttons_row1, buttons_row2]

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    guild = bot.guilds[0]
    channel = discord.utils.get(guild.channels, name='mecs')

    if channel is None:
        print("Channel not found")
        return

    action_row1 = [
        create_button(style=ButtonStyle.green, label="Logar", custom_id="logar_button"),
        *[
            create_button(style=ButtonStyle.blue, label=activity, custom_id=activity.lower().replace(" ", "_"))
            for activity in ACTIVITIES[:5]
        ]
    ]

    action_row2 = [
        *[
            create_button(style=ButtonStyle.blue, label=activity, custom_id=activity.lower().replace(" ", "_"))
            for activity in ACTIVITIES[5:10]
        ]
    ]

    message = await channel.send("Controle de atividades da Mecanica:", components=[action_row1, action_row2])
    messages[message.id] = set()

    print(f"Message created: {message.id}")



@bot.event
async def on_button_click(interaction):
    await interaction.respond(type=6)

bot.run(TOKEN)

