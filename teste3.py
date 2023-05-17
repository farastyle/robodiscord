import discord

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    channel = client.get_channel(1103535910072635414)  # substitua pelo ID do canal desejado
    message = await channel.send("Nenhum usuário logado no momento.", 
                                 components=[Button(style=ButtonStyle.green, label="Logar", custom_id="logar_button"),
                                             Button(style=ButtonStyle.red, label="Deslogar", custom_id="deslogar_button")])
    print(f"Bot iniciado e mensagem enviada: {message.content}")

async def update_status_message(message, logged_in_users):
    if logged_in_users:
        logged_in_users_str = "\n".join(logged_in_users)
        status_message = f"Usuários logados:\n{logged_in_users_str}"
    else:
        status_message = "Nenhum usuário logado no momento."
    await message.edit(content=status_message)

logged_in_users = set()

@client.event
async def on_button_click(interaction):
    global logged_in_users
    if interaction.custom_id == "logar_button":
        user = interaction.user.display_name
        logged_in_users.add(user)
        await interaction.message.clear_reactions()
        await interaction.message.add_reaction("✅")
        await update_status_message(interaction.message, logged_in_users)
    elif interaction.custom_id == "deslogar_button":
        user = interaction.user.display_name
        logged_in_users.discard(user)
        await interaction.message.clear_reactions()
        await interaction.message.add_reaction("❌")
        await update_status_message(interaction.message, logged_in_users)

client.run("MTEwNDUzNTQwNTU3NzEwOTU0NA.GkdmiH.MaP79EubpVnqgAHvinAxFPX1KPUvXwv-86tVj0")
