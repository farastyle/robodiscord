import discord
from discord.ext import commands
from discord import Button
client = discord.Client(intents=discord.Intents.all())
intents = discord.Intents.default()
intents.members = True
status_message_id = None

bot = commands.Bot(command_prefix='!', intents=intents)
def create_button(label, style, custom_id):
     return Button(style=style, label=label, custom_id=custom_id)


async def update_status_message(channel, logged_in_users):
    members = await get_logged_in_members(channel.guild)
    if members:
        status_message = "```Usuários ativos: \n" + "\n".join([m for m in members if m in logged_in_users]) + "```"
    else:
        status_message = "```Nenhum usuário ativo no momento.```"
    message = await channel.history().get(author=client.user)
    await message.edit(components=[create_button_row(logged_in_users), discord.Embed(description=status_message, color=0x00FF00)])

async def get_logged_in_members(guild):
    logged_in_users = []
    for member in guild.members:
        if member.status != discord.Status.offline:
            logged_in_users.append(member.display_name)
    return logged_in_users

def create_button_row(logged_in_users):
    buttons_row1 = [discord.Button(style=discord.ButtonStyle.success, label="Logar", custom_id="logar_button"),
                    discord.Button(style=discord.ButtonStyle.danger, label="Deslogar", custom_id="deslogar_button")]
    if len(logged_in_users) > 0:
        buttons_row1.insert(1, Button(style=ButtonStyle.grey, label=f"{len(logged_in_users)} usuários em serviço", disabled=True))
    return buttons_row1

@client.event
async def on_ready():
    channel = client.get_channel(1103535910072635414)  # substitua pelo ID do canal desejado
    message = await channel.send("Controle de atividades da Mecanica:", components=[create_button_row(set())])
    print(f"Bot iniciado e mensagem enviada: {message.content}")
    await update_status_message(channel, set())

logged_in_users = set()

@client.event
async def on_button_click(interaction):
    global logged_in_users
    if interaction.custom_id == "logar_button":
        user = interaction.user.display_name
        logged_in_users.add(user)
        await interaction.message.clear_reactions()
        await interaction.message.add_reaction("✅")
        await update_status_message(interaction.message.channel, logged_in_users)
    elif interaction.custom_id == "deslogar_button":
        user = interaction.user.display_name
        logged_in_users.discard(user)
        await interaction.message.clear_reactions()
        await interaction.message.add_reaction("❌")
        await update_status_message(interaction.message.channel, logged_in_users)


client.run("Hidden")
