import os
from datetime import datetime
import discord
from discord_slash import SlashCommand
from discord_components import DiscordComponents, Button, ButtonStyle

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
DiscordComponents(client)


def create_button(label, style, custom_id):
    return Button(style=style, label=label, custom_id=custom_id)


async def update_status_message(channel, checked_in_users):
    count = len(checked_in_users)
    status_message = f"Checked-in Users: {count}\n\n"
    for user in checked_in_users:
        status_message += f"{user['name']} checked-in at {user['time']}\n"
    checkin_button = create_button(label="Check-in", style=ButtonStyle.green, custom_id="checkin")
    checkout_button = create_button(label="Check-out", style=ButtonStyle.red, custom_id="checkout")
    await channel.send(
        embed=discord.Embed(description=status_message, color=0x00FF00),
        components=[[checkin_button, checkout_button]]
    )


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(guild.channels, name="general")
    await update_status_message(channel, set())


@client.event
async def on_button_click(interaction):
    channel = client.get_channel(interaction.channel_id)
    message = await channel.fetch_message(interaction.message.id)
    checked_in_users = set()
    for component in message.components:
        for button in component.components:
            if button.style == ButtonStyle.green and interaction.custom_id == "checkin":
                checked_in_users.add({"name": interaction.author.display_name, "time": datetime.now().strftime("%H:%M:%S")})
            elif button.style == ButtonStyle.red and interaction.custom_id == "checkout":
                checked_in_users.discard({"name": interaction.author.display_name, "time": datetime.now().strftime("%H:%M:%S")})
    await update_status_message(channel, checked_in_users)

client.run("HIDDEN")
