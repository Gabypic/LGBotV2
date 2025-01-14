import discord
from discord.ext import commands
from discord.ui import View, Select
from Database.databasehandler import DatabaseHandler
from distribution import SP
import classNotLoop
import asyncio


DatabaseHandler = DatabaseHandler("database.db")


async def Chasseur(interaction, Bot):
    player_list = DatabaseHandler.alive_player_list()
    classNotLoop.one_time_role.chasseur_played = True
    allowed_player = DatabaseHandler.name_for_role(f"Chasseur {SP.Chasseur}")
    userid = int(DatabaseHandler.discordID_for_name(allowed_player))
    user = await Bot.fetch_user(userid)
    chosen_one = []
    chose = asyncio.Event()

    msg = discord.Embed(title=f"Tu est mort, en tant que chasseur, tu peux emporter quelqu'un dans la mort !",
                        colour=0x95D72A)
    msg.add_field(name="tips",
                  value=f"**/liste_des_joueurs** pour connaitre la liste des joueurs ainsi que leur numéro.")

    options = [discord.SelectOption(label=value) for value in player_list]
    select = Select(placeholder="Choisis un joueur", options=options)

    async def select_callback(interaction):
        confirmation_msg = discord.Embed(
            title=f"Tu as tirer sur {select.values[0]}",
            colour=0x95D72A
        )
        await interaction.response.send_message(embed=confirmation_msg)
        chosen_one.append(select.values[0])
        chose.set()

    select.callback = select_callback
    view = View()
    view.add_item(select)
    await user.send(embed=msg, view=view)

    await chose.wait()
    chosen_one = DatabaseHandler.number_for_name(chosen_one[0])

    return chosen_one
