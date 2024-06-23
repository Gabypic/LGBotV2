import discord
from discord.ext import commands
from Database.databasehandler import DatabaseHandler
from distribution import SP
import classNotLoop
from checks import check_slash_wait

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot

class voted_player:
    Cupi_touched = []


async def Cupidon(interaction, Bot):
    classNotLoop.one_time_role.Cupidon_played = True
    allowed_player = DatabaseHandler.name_for_role(f"Cupidon {SP.Cupidon}")
    userid = int(DatabaseHandler.discordID_for_name(allowed_player))
    user = await Bot.fetch_user(userid)
    msg = discord.Embed(title="Qui veut tu toucher de tes flèches afin de les liés à jamais ?", colour=0x00FF00)
    msg.add_field(name=f"",value=f"Envoie les numéros des joueurs que tu veux toucher de ta flèche")
    await user.send(embed=msg)

    def check(message):
        return message.author == user and isinstance(message.channel, discord.DMChannel)

    i = 0
    while i != 2:
        chosen_one = await Bot.wait_for('message', check=check)
        if DatabaseHandler.no_number(chosen_one.content):
            voted_player.Cupi_touched.append(chosen_one.content)
            print("No number")
            print(voted_player.Cupi_touched)
            if i == 1:
                print("not added 1st")
                print(voted_player.Cupi_touched)
                if voted_player.Cupi_touched[0] == voted_player.Cupi_touched[1]:
                    del voted_player.Cupi_touched[1]
                    msg = discord.Embed(title=f"Tu à déjà choisi ce joueur", colour=0xFF0000)
                    await user.send(embed=msg)
                    i = 1
                else:
                    print("added 2nd")
                    print(voted_player.Cupi_touched)
                    i += 1
                    DatabaseHandler.add_couple(chosen_one.content)
            else:
                print("added 1st")
                print(voted_player.Cupi_touched)
                i += 1
                DatabaseHandler.add_couple(chosen_one.content)
        else:
            print("inexistant")
            print(voted_player.Cupi_touched)
            msg = discord.Embed(title="Ce joueur n'éxiste pas !", colour=0xFF0000)
            msg.add_field(name="",value=f"Utilise **/liste_des_joueurs** pour connaitre la liste des joueurs et leurs numéros")
            await user.send(embed=msg)

    msg = discord.Embed(title="Les deux amoureux ont été touchés par tes flèches !", colour=0xFD6C9E)
    print(voted_player.Cupi_touched)
    msg.add_field(name=f"{DatabaseHandler.name_for_number(voted_player.Cupi_touched[0])}", value="")
    msg.add_field(name=f"{DatabaseHandler.name_for_number(voted_player.Cupi_touched[1])}", value="")
    await user.send(embed=msg)
    classNotLoop.one_time_role.Cupidon_played = True