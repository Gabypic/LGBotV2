import discord
from discord.ext import commands
from Database.databasehandler import DatabaseHandler
from distribution import SP
from checks import check_slash_wait

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot

class sorciere_var:
    heal = False
    kill = False

async def Sorciere(interaction, Bot, died: int):
    allowed_player = DatabaseHandler.name_for_role(f"Sorciere {SP.Sorciere}")
    userid = int(DatabaseHandler.discordID_for_name(allowed_player))
    user = await Bot.fetch_user(userid)

    def check_private_message(message):
        return message.author == user and isinstance(message.channel, discord.DMChannel)

    if died == 0:
        died_one = "personne n'" #quasi impossible mais au cas ou (ligne 219)
    else:
        died_one = DatabaseHandler.name_for_number(str(died))
    if not sorciere_var.heal and not sorciere_var.kill and int(died) > 0:
        msg = discord.Embed(title=f"{died_one} est mort cette nuit!", colour=0xFF8700)
        msg.add_field(name="1", value=f"Tu peux le sauver !")
        msg.add_field(name="2", value=f"Tuer quelqu'un d'autre !")
        msg.add_field(name="3", value="Ou bien ne rien faire.")
        await user.send(embed=msg)

    if not sorciere_var.heal and sorciere_var.kill and died > 1:
        msg = discord.Embed(title=f"{died_one} est mort cette nuit!", colour=0xFF8700)
        msg.add_field(name="1", value=f"Tu peux le sauver !")
        msg.add_field(name="3", value="Ou bien ne rien faire.")
        await user.send(embed=msg)

    if sorciere_var.heal or died == 0 and not sorciere_var.kill:
        msg = discord.Embed(title=f"{died_one} est mort cette nuit!", colour=0xFF8700)
        msg.add_field(name="2", value=f"Tu peux tuer quelqu'un d'autre !")
        msg.add_field(name="3", value="Ou bien ne rien faire.")
        await user.send(embed=msg)

    if (sorciere_var.heal and sorciere_var.kill) or (died == 0 and sorciere_var.kill):
        msg = discord.Embed(title=f"{died_one} est mort cette nuit!", colour=0xFF8700)
        msg.add_field(name="Tu n'a plus de potions", value=f"Tu as utilisé toutes tes potions !")
        await user.send(embed=msg)
        return 0

    potion_choice = await Bot.wait_for('message', check=check_private_message)
    potion_use = int(potion_choice.content)
    if potion_use == 1 and not sorciere_var.heal and int(died) > 0:
        msg = discord.Embed(title=f"Tu as sauvé {died_one}", colour=0x00FF00)
        await user.send(embed=msg)
        sorciere_var.heal = True
        return 0
    if potion_use == 1 and sorciere_var.heal and int(died) > 0:
        msg = discord.Embed(title=f"Tu à déjà utilisé ta potion de vie !", colour=0xFF0000)
        await user.send(embed=msg)
        await Sorciere(interaction, Bot, died)
    if potion_use == 1 and not sorciere_var.heal and died ==0:
        msg = discord.Embed(title=f"Action impossible !", colour=0xFF0000)
        msg.add_field(name="Tu ne peux pas utiliser ta potion si personne n'est mort.", value="")

    if potion_use == 2 and not sorciere_var.kill:
        msg = discord.Embed(title=f"Qui veut tu éliminer ?", colour=0xFF0000)
        msg.add_field(name=f"Information", value=f"/liste_des_joueurs pour voir la liste des joueurs et leur numéro")
        await user.send(embed=msg)
        check = False
        while not check:
            kill = await Bot.wait_for('message', check=check_private_message)
            check = check_slash_wait(kill)
        msg = discord.Embed(title=f"Tu à décidé de tuer {DatabaseHandler.name_for_number(kill.content)} ! ", colour=0x000000)
        await user.send(embed=msg)
        sorciere_var.kill = True
        return kill.content
    if potion_use == 2 and sorciere_var.kill:
        msg = discord.Embed(title=f"Tu as déjà utilisé ta potion de mort !", colour=0xFF0000)
        await user.send(embed=msg)
        await Sorciere(interaction, Bot, died)

    if potion_use == 3:
        msg = discord.Embed(title=f"Tu as décidé de ne rien faire cette nuit.", colour=0x0000FF)
        await user.send(embed=msg)

    if potion_use <=0 or potion_use > 3:
        msg = discord.Embed(title="Tu ne peux choisir qu'entre 1, 2 et 3 !", colour=0xFF0000)
        await user.send(embed=msg)