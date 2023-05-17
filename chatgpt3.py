import discord
from discord.ext import commands
import utils
import settings


class SimpleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.foo = None
        self.trabalhando = []
        # self.add_item(discord.ui.Button(label="Entrar", style=discord.ButtonStyle.green, custom_id="entrar_button"))
        # self.add_item(discord.ui.Button(label="Sair", style=discord.ButtonStyle.red, custom_id="sair_button"))

    async def update_message(self, interaction: discord.Interaction):
        await interaction.message.edit(content=f"```Mecânicos trabalhando: \n" + "\n".join([member.display_name for member in self.trabalhando] + "```"))

    @discord.ui.button(label="Entrar", style=discord.ButtonStyle.green, custom_id="entrar_button")
    async def enter_button(self, button: discord.ui.Button, interaction: discord.Interaction):
     member = interaction.user
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    self.trabalhando.append(f"{member.name} - {current_time}")
    await interaction.response.edit_message(view=self)


    @discord.ui.button(label="Sair", style=discord.ButtonStyle.red, custom_id="sair_button")
    async def exit_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        member = interaction.user
        if member in self.trabalhando:
            self.trabalhando.remove(member)
        await self.update_message(interaction)


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
    await interaction.message.view(interaction)


bot.run(settings.DISCORD_API_SECRET, root_logger=True)
