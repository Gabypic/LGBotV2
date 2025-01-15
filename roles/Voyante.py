import discord
from discord.ext import commands
from discord.ui import Button, Select, View
import asyncio
from Database.databasehandler import DatabaseHandler
from distribution import SP

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot


async def Voyante(interaction, Bot):
    player_list = DatabaseHandler.alive_player_list()
    allowed_player = DatabaseHandler.name_for_role(f"Voyante {SP.Voyante}")
    userid = int(DatabaseHandler.discordID_for_name(allowed_player))
    user = await Bot.fetch_user(userid)
    chosen_one = []
    chose = asyncio.Event()

    msg = discord.Embed(
        title=f"Quel joueur veux-tu observer cette nuit ?",
        colour=0xA71DE1
    )
    msg.add_field(
        name="info",
        value="Vote pour une cible en la choisissant dans la liste déroulante."
    )
    options = [discord.SelectOption(label=value) for value in player_list]
    select = Select(placeholder="Choisis un joueur !", options=options)

    async def select_callback(interaction):
        confirmation_msg = discord.Embed(
            title=f"Tu vas observer {select.values[0]}:",
            colour=0x00FF00
        )
        print(f"Selected value: {select.values[0]}")
        await interaction.response.send_message(embed=confirmation_msg)
        chosen_one.append(select.values[0])
        chose.set()

    select.callback = select_callback
    view = View()
    view.add_item(select)
    await user.send(embed=msg, view=view)

    await chose.wait()
    chosen_one = chosen_one[0]
    role = DatabaseHandler.role_for_name(chosen_one)

    if role == f"Loup-Garou {SP.LG}":
        msg = discord.Embed(
            title=f"{chosen_one}",
            colour=0xFF0000
        )
        msg.add_field(name=f"{role}", value="")
        await user.send(embed=msg)

    else:
        msg = discord.Embed(
            title=f"{chosen_one}",
            colour=0x00FF00
        )
        msg.add_field(name=f"{role}", value="")
        await user.send(embed=msg)
