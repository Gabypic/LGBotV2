import discord
import asyncio
from discord.ext import commands
from discord.ui import View, Select
from Database.databasehandler import DatabaseHandler
from distribution import SP
import classNotLoop
from checks import check_slash_wait

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot

class voted_player:
    Cupi_touched = []


async def Cupidon(interaction, Bot):
    allowed_player = DatabaseHandler.name_for_role(f"Cupidon {SP.Cupidon}")
    userid = int(DatabaseHandler.discordID_for_name(allowed_player))
    user = await Bot.fetch_user(userid)
    player_list = DatabaseHandler.alive_player_list()
    first_choice = asyncio.Event()
    second_choice = asyncio.Event()

    first_msg = discord.Embed(
        title="Qui veut tu toucher de tes flèches afin de les lier à jamais ?",
        colour=0x00FF00
    )
    first_msg.add_field(
        name="Première cible",
        value = "Qui veut tu toucher de ta première flèche ?"
    )
    first_msg.add_field(
        name="info",
        value="Vote pour une cible en la choisissant dans la liste déroulante."
    )
    options = [discord.SelectOption(label=value) for value in player_list]
    first_select = Select(placeholder="Choisis le premier amoureux", options=options)

    async def first_select_callback(interaction):
        confirmation_msg = discord.Embed(
            title=f"Le premier amoureux est {first_select.values[0]}",
            colour=0xFD6C9E
        )

        await interaction.response.send_message(embed=confirmation_msg)
        voted_player.Cupi_touched.append(first_select.values[0])
        first_choice.set()

    first_select.callback = first_select_callback
    view = View()
    view.add_item(first_select)
    await user.send(embed=first_msg, view=view)
    await first_choice.wait()

    player_list.remove(voted_player.Cupi_touched[0])

    second_msg = discord.Embed(
        title="Qui veut tu toucher de tes flèches afin de les lier à jamais ?",
        colour=0x00FF00
    )
    second_msg.add_field(
        name="Deuxième cible",
        value="Qui veut tu toucher de ta deuxième flèche ?"
    )
    second_msg.add_field(
        name="info",
        value="Vote pour une cible en la choisissant dans la liste déroulante."
    )

    options = [discord.SelectOption(label=label) for label in player_list]
    second_select = Select(placeholder="Choisis le deuxième amoureux", options=options)

    async def second_select_callback(interaction):
        confirmation_msg = discord.Embed(
            title=f"Le deuxième amoureux est {second_select.values[0]}",
            colour=0xFD6C9E
        )
        confirmation_msg.add_field(
            name="Le couple est formé !",
            value=f"Tu viens de lier à jamais {voted_player.Cupi_touched[0]} et {second_select.values[0]} :heart: \n"
                  f"Si l'un des deux meurt, l'autre le rejoindra dans la mort."
        )
        await interaction.response.send_message(embed=confirmation_msg)
        voted_player.Cupi_touched.append(second_select.values[0])
        second_choice.set()

    second_select.callback = second_select_callback
    view = View()
    view.add_item(second_select)
    await user.send(embed=second_msg, view=view)
    await second_choice.wait()
    for lover in voted_player.Cupi_touched:
        DatabaseHandler.add_couple(DatabaseHandler.number_for_name(lover))

    print(voted_player.Cupi_touched)
    classNotLoop.one_time_role.Cupidon_played = True
