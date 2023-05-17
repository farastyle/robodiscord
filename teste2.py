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
            texto1.append(interaction.user.display_name)
            texto2.append(f"{interaction.user.display_name} entrou às {datetime.now().strftime('%H:%M:%S')}")
            view = MyView()
            await interaction.message.edit(embed=get_embed(), view=view)
        await interaction.response.defer()

    @discord.ui.button(label="Sair", style=discord.ButtonStyle.red, custom_id="sair")
    async def sair_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name in texto1:
            texto1.remove(interaction.user.display_name)
            texto2.append(f"{interaction.user.display_name} saiu às {datetime.now().strftime('%H:%M:%S')}")
            view = MyView()
            await interaction.message.edit(embed=get_embed(), view=view)
        await interaction.response.defer()


async def update_message(channel):
    # create a MyView object with the buttons
    view = MyView()
    # create an Embed object with initial information
    embed = discord.Embed(title='Distritao Mecânica, registro de funcionários e log de atividade', color=0x00ff00)
    embed.add_field(name='Quem está trabalhando:', value='Loading...', inline=False)
    embed.add_field(name='Log de chegada e saída:', value='Loading...', inline=False)
    # send the message with the view and embed objects
    message = await channel.send(embed=embed, view=view)
    # update the message with the actual data
    embed = get_embed()
    await message.edit(embed=embed, view=view)


def get_embed():
    embed = discord.Embed(title='Delta point, Cadastro de horas', color=0x00ff00)
    embed.add_field(name='Quem está trabalhando:', value='\n'.join(texto1) if texto1 else 'Ninguém')
    embed.add_field(name='Log de chegada e saída:', value='\n'.join(texto2) if texto2 else 'Nenhum registro ainda')
    return embed




@bot.event
async def on_ready():
    print('Bot está online')
    channel = bot.get_channel(1105561415038812311) # Insira aqui o ID do canal em que o bot deve ficar
    await update_message(channel)

bot.run(settings.DISCORD_API_SECRET)
