import discord
from discord.ext import commands
import utils
import settings


class SimpleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.foo = None
        self.add_item(discord.ui.Button(label="Entrar", style=discord.ButtonStyle.green, custom_id="Entrar_button"))
        self.add_item(discord.ui.Button(label="Sair", style=discord.ButtonStyle.red, custom_id="Sair_button"))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    guild = bot.get_guild(settings.GUILD_ID_INT)
    view = SimpleView()
    message = await guild.get_channel(settings.FEEDBACK_CH).send(view=view)
    await guild.get_channel(settings.FEEDBACK_CH).send("Mecânicos trabalhando:")


@bot.event
async def on_button_click(interaction: discord.Interaction):
    await interaction.response.defer()
    member = interaction.user
    await interaction.message.edit(content=f"Mecânicos trabalhando: \n {member.display_name}")

bot.run(settings.DISCORD_API_SECRET, root_logger=True)