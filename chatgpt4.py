import discord
from discord.ext import commands
import utils
import settings
from datetime import datetime

class SimpleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.foo = None
        self.trabalhando = []

        self.entrar_button = discord.ui.Button(label="Entrar", style=discord.ButtonStyle.green, custom_id="entrar_button")
        self.add_item(self.entrar_button)

        self.sair_button = discord.ui.Button(label="Sair", style=discord.ButtonStyle.red, custom_id="sair_button")
        self.add_item(self.sair_button)

    async def update_message(self, interaction: discord.Interaction):
        await interaction.message.edit(content=f"```Mecânicos trabalhando: \n" + "\n".join([member.display_name for member in self.trabalhando] + "```"))

    async def enter_button_callback(self, interaction: discord.Interaction):
        member = interaction.user
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.trabalhando.append(f"{member.name} - {current_time}")
        await interaction.response.edit_message(view=self)

    async def exit_button_callback(self, interaction: discord.Interaction):
        member = interaction.user
        if member in self.trabalhando:
            self.trabalhando.remove(member)
        await self.update_message(interaction)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    guild = bot.get_guild(settings.GUILD_ID_INT)
    view = SimpleView()
    message = await guild.get_channel(settings.FEEDBACK_CH).send(view=view)
    await guild.get_channel(settings.FEEDBACK_CH).send("Mecânicos trabalhando:")

@bot.event
async def on_button_click(interaction: discord.Interaction):
    if interaction.custom_id.startswith('entrar_button'):
        view = SimpleView()
        await view.enter_button_callback(interaction)
    elif interaction.custom_id.startswith('sair_button'):
        view = SimpleView()
        await view.exit_button_callback(interaction)
    else:
        await interaction.response.send_message("Unknown button clicked.", ephemeral=True)

bot.run(settings.DISCORD_API_SECRET, root_logger=True)
