import os
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!')
status_message_id = None


def create_button(label, style, custom_id):
    return Button(style=style, label=label, custom_id=custom_id)


async def update_status_message():
    global status_message_id
    channel = bot.get_channel(1103535910072635414)
    if status_message_id is None:
        message = await channel.send("React to check-in!", components=[create_button("Check-in", ButtonStyle.green, "checkin")])
        status_message_id = message.id
    else:
        message = await bot.get_channel(1103535910072635414).fetch_message(status_message_id)
        count = len([r for r in message.reactions if str(r.emoji) == "✅"])
        message_embed = message.embeds[0]
        message_embed.set_field_at(0, name="Attendance", value=f"{count}/100")
        await message.edit(embed=message_embed)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await update_status_message()


@bot.event
async def on_button_click(interaction):
    channel = bot.get_channel(1103535910072635414)
    if interaction.component.id == "checkin":
        user = {"name": interaction.author.display_name, "time": str(interaction.created_at.time())[:-7]}
        await interaction.respond(type=InteractionType.UpdateMessage, embed=discord.Embed(title=f"{user['name']} has checked-in!", description=f"Time: {user['time']}"), components=[])
        await update_status_message()
    else:
        await interaction.respond(type=InteractionType.UpdateMessage, embed=discord.Embed(title="Unknown Button Clicked"), components=[])

client.run("Hidden")
