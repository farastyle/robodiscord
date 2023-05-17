# This example requires the 'message_content' privileged intent to function.
import discord
import asyncio
import os
from discord.ext import commands
import settings
from datetime import datetime
os.environ["X"] = "0"

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        x = int(os.environ["X"])  # Retrieve value of environment variable 'X'
        if message.content.startswith('!editme'):
            await asyncio.sleep(3.0)
            x = x + 1
            await msg.edit(content=x)
            os.environ["X"] = str(x)  # Update value of environment variable 'X'

    # async def on_message_edit(self, before, after):
    #     msg = f'**{before.author}** edited their message:\n{before.content} -> {after.content}'
    #     await before.channel.send(msg)
    async def on_ready(self):
        x = int(os.environ.get("X", 0))  # Retrieve value of environment variable 'X' or set to 0 if it doesn't exist
        msg = await channel.send(f"{x}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(settings.DISCORD_API_SECRET, root_logger=True)
