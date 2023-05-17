import discord
from discord.ext import commands
from datetime import datetime
import settings

texto1 = []
texto2 = []
bot = discord.Client(intents=discord.Intents.all())
class MyView(discord.ui.View):
    @discord.ui.button(label="Entrar", style=discord.ButtonStyle.green, custom_id="entrar")
    async def entrar_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name not in texto1:
            view = MyView()
            texto1.append(interaction.user.display_name)
            texto2.append(f"{interaction.user.display_name} entrou às {datetime.now().strftime('%H:%M:%S')}")
            
            await interaction.message.edit(content=get_text())
        await interaction.response.defer()

    @discord.ui.button(label="Sair", style=discord.ButtonStyle.red, custom_id="sair")
    async def sair_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name in texto1:
            view = MyView()
            texto1.remove(interaction.user.display_name)
            texto2.append(f"{interaction.user.display_name} saiu às {datetime.now().strftime('%H:%M:%S')}")
            
            await interaction.message.edit(content=get_text())
        await interaction.response.defer()


async def update_message(channel):
    
    text = get_text()
    message = await channel.send(text)
    # update the message with the actual data
    text = get_text()
    await message.edit(content=text)

async def buttons(channel):
    # create a MyView object with the buttons
    view = MyView()
    # create an initial message
    message = await channel.send(view=view)
    # update the message with the actual data
    


def get_text():
    text1 = '\n'.join(texto1) if texto1 else 'Ninguém'
    text2 = '\n'.join(texto2) if texto2 else 'Nenhum registro ainda'
    text = f"**Quem está trabalhando:**\n{text1}\n\n**Log de chegada e saída:**\n{text2}"
    return text






@bot.event
async def on_ready():
    print('Bot está online')
    channel = bot.get_channel(1105561415038812311) # Insira aqui o ID do canal em que o bot deve ficar
    await buttons(channel)
    await update_message(channel)

bot.run(settings.DISCORD_API_SECRET)
