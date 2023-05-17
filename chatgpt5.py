import discord
from discord.ext import commands
import settings
from datetime import datetime


class SimpleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.foo = None
        self.trabalhando = []

        self.entrar_button = discord.ui.Button(label="Entrar", style=discord.ButtonStyle.green, custom_id="entrar_button")
        self.add_item(self.entrar_button)

        self.sair_button = discord.ui.Button(label="Sair", style=discord.ButtonStyle.red, custom_id="sair_button")
        self.add_item(self.sair_button)
        for item in self.children:
            item.custom_id = item.custom_id or f"{item.label}-{item.style}" # set custom_id if not already set

    async def update_message(self, interaction: discord.Interaction):
        await interaction.message.edit(content=f"```Mecânicos trabalhando: \n" + "\n".join([member.display_name for member in self.trabalhando]) + "```")
        

    async def enter_button_callback(self, interaction: discord.Interaction):
        member = interaction.user
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.trabalhando.append(member)
        await self.update_message(interaction)
        

    async def exit_button_callback(self, interaction: discord.Interaction):
        member = interaction.user
        if member in self.trabalhando:
            self.trabalhando.remove(member)
        await self.update_message(interaction)
    
    def print_trabalhando(self):
        print(self.trabalhando)
        for member in self.trabalhando:
            print(f"{member.display_name}")


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    guild = bot.get_guild(settings.GUILD_ID_INT)
    view = SimpleView()
    view.print_trabalhando()
    message = await guild.get_channel(settings.FEEDBACK_CH).send(view=view)
    await guild.get_channel(settings.FEEDBACK_CH).send("```Mecânicos trabalhando:```")


# @bot.event
# async def on_button_click(interaction: discord.Interaction):
#     await interaction.response.defer()

#     if interaction.custom_id.startswith('entrar_button'):
#         view = SimpleView()
#         await view.enter_button_callback(interaction)
#         await view.enter_button_callback(interaction)
#         print(view.trabalhando)
#     elif interaction.custom_id.startswith('sair_button'):
#         view = SimpleView()
#         await view.exit_button_callback(interaction)
#     else:
#         await interaction.response.send_message("Unknown button clicked.", ephemeral=True)


@bot.event
async def on_ready():
    guild = bot.get_guild(settings.GUILD_ID_INT)
    view = SimpleView()
    view.print_trabalhando()
    message = await guild.get_channel(settings.FEEDBACK_CH).send(view=view)
    await guild.get_channel(settings.FEEDBACK_CH).send("```Mecânicos trabalhando:```")
    bot.add_view(view) # add the view to the bot so it can listen for button clicks

@bot.event
async def on_interaction(interaction: discord.Interaction):
    view = bot.views[0] # get the first view added to the bot
    await interaction.response.defer()

    if interaction.custom_id.startswith('entrar_button'):
        await view.enter_button_callback(interaction)
        print(view.trabalhando)
    elif interaction.custom_id.startswith('sair_button'):
        await view.exit_button_callback(interaction)
    else:
        await interaction.response.send_message("Unknown button clicked.", ephemeral=True)


bot.run(settings.DISCORD_API_SECRET, root_logger=True)