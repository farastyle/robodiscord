import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

client = commands.Bot(command_prefix='!')
logged_in_users = set()

@client.event
async def on_ready():
    DiscordComponents(client)
    channel = client.get_channel(1103535910072635414)  # Substitua pelo ID do canal que você deseja enviar a mensagem

    checkin_button = Button(style=ButtonStyle.green, label="Check-in", id="checkin")
    checkout_button = Button(style=ButtonStyle.red, label="Check-out", id="checkout")
    await channel.send(content="Controle de atividades da Mecanica:", components=[checkin_button, checkout_button])

    global status_message
    status_message = "Ninguém logado"

    await update_status_message(channel, set())

async def update_status_message(channel, logged_in_users):
    global status_message

    if not logged_in_users:
        status_message = "Ninguém logado"
    else:
        user_list = "\n".join([f"{user['name']} ({user['time']})" for user in logged_in_users])
        status_message = f"Usuários logados:\n{user_list}"

    message = await channel.fetch_message(channel.last_message_id)

    # Cria os botões de Check-in e Check-out novamente para atualizar a mensagem
    checkin_button = Button(style=ButtonStyle.blue, label="Check-in", id="checkin")
    checkout_button = Button(style=ButtonStyle.red, label="Check-out", id="checkout")

    await message.edit(components=[checkin_button, checkout_button, discord.Embed(description=status_message, color=0x00FF00)])

@client.event
async def on_button_click(interaction):
    global logged_in_users

    if interaction.component.id == "checkin":
        user = {"name": interaction.author.display_name, "time": str(interaction.created_at.time())[:-7]}
        logged_in_users.add(user)
        await interaction.respond(content=f"Check-in realizado por {interaction.author.display_name}!")
    elif interaction.component.id == "checkout":
        for user in logged_in_users:
            if user["name"] == interaction.author.display_name:
                logged_in_users.remove(user)
                await interaction.respond(content=f"Check-out realizado por {interaction.author.display_name}!")
                break

    await update_status_message(interaction.channel, logged_in_users)

client.run("MTEwNDUzNTQwNTU3NzEwOTU0NA.G3WnyQ.v3boFAdHR6DvPZ6MsgOy2MLvTSep-wqCxF33T8")
