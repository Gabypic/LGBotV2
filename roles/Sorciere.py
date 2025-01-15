from cProfile import label

import discord
from discord.ext import commands
from discord.ui import Select, View
from Database.databasehandler import DatabaseHandler
from distribution import SP
from checks import check_slash_wait
import asyncio

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot

class sorciere_var:
    heal = False
    kill = False


async def Sorciere(interaction, Bot, died: int):
    allowed_player = DatabaseHandler.name_for_role(f"Sorciere {SP.Sorciere}")
    userid = int(DatabaseHandler.discordID_for_name(allowed_player))
    user = await Bot.fetch_user(userid)
    potion_choice = []
    potion_choice_callback = asyncio.Event()

    if died == 0:
        died_one = "personne n'"  # quasi impossible mais au cas ou (ligne 41)
    else:
        died_one = DatabaseHandler.name_for_number(str(died))

    msg = discord.Embed(title=f"{died_one} est mort cette nuit", colour=0xFF8700)
    potion_options = usable_potions(died)
    potion_select = Select(placeholder="Choisis ton action", options=potion_options)

    async def select_potion_callback(interaction):
        confirmation_msg = discord.Embed(
            title=f"{potion_select.values[0]}", colour=0xFF0000
        )
        await interaction.response.send_message(embed=confirmation_msg)
        potion_choice.append(potion_select.values[0])
        potion_choice_callback.set()

    potion_select.callback = select_potion_callback
    view = View()
    view.add_item(potion_select)
    await user.send(embed=msg, view=view)
    await potion_choice_callback.wait()
    chosen_potion = potion_choice[0]

    if used_potion(chosen_potion) == 1:
        msg = discord.Embed(title=f"Tu as sauvé {died_one}", colour=0x00FF00)
        await user.send(embed=msg)
        sorciere_var.heal = True
        return 0

    if used_potion(chosen_potion) == 0:
        msg = discord.Embed(title=f"Tu as décidé de ne rien faire cette nuit.", colour=0x0000FF)
        await user.send(embed=msg)

    if used_potion(chosen_potion) == 2:
        player_list = DatabaseHandler.alive_player_list()
        kill_choice = []
        kill_choice_callback = asyncio.Event()
        msg = discord.Embed(title=f"Qui veut tu éliminer ?", colour=0xFF0000)

        kill_options = [discord.SelectOption(label=value) for value in player_list]
        kill_select = Select(placeholder="Choisis un joueur", options=kill_options)

        async def select_kill_callback(interaction):
            confirmation_msg = discord.Embed(
                title=f"Tu as décider de tuer {kill_select.values[0]}", colour=0xFF0000
            )
            await interaction.response.send_message(embed=confirmation_msg)
            kill_choice.append(kill_select.values[0])
            kill_choice_callback.set()

        kill_select.callback = select_kill_callback
        view = View()
        view.add_item(kill_select)
        await user.send(embed=msg, view=view)

        await kill_choice_callback.wait()

        return DatabaseHandler.number_for_name(kill_select.values[0])



def used_potion(potion):
    if potion == "Tu peux le sauver":
        return 1
    if potion == "Tuer quelqu'un d'autre":
        return 2
    if potion == "Ne rien faire":
        return 0


def usable_potions(died):
    options = []

    if not sorciere_var.heal and not sorciere_var.kill and int(died) > 0:
        options.append(discord.SelectOption(label="Tu peux le sauver"))
        options.append(discord.SelectOption(label="Tuer quelqu'un d'autre"))
        options.append(discord.SelectOption(label="Ne rien faire"))

    elif not sorciere_var.heal and sorciere_var.kill and int(died) > 0:
        options.append(discord.SelectOption(label="Tu peux le sauver"))
        options.append(discord.SelectOption(label="Ne rien faire"))

    elif sorciere_var.heal and not sorciere_var.kill:
        options.append(discord.SelectOption(label="Tuer quelqu'un d'autre"))
        options.append(discord.SelectOption(label="Ne rien faire"))

    elif sorciere_var.heal and sorciere_var.kill:
        options.append(discord.SelectOption(label="Ne rien faire"))

    return options

