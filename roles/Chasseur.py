import discord
from discord.ext import commands
from Database.databasehandler import DatabaseHandler
from distribution import SP
import classNotLoop


DatabaseHandler = DatabaseHandler("database.db")


async def Chasseur(interaction, Bot):
    classNotLoop.one_time_role.chasseur_played = True
    allowed_player = DatabaseHandler.name_for_role(f"Chasseur {SP.Chasseur}")
    userid = int(DatabaseHandler.discordID_for_name(allowed_player))
    user = await Bot.fetch_user(userid)
    msg = discord.Embed(title=f"Tu est mort, en tant que chasseur, tu peux emporter quelqu'un dans la mort !",
                        colour=0x95D72A)
    msg.add_field(name="tips",
                  value=f"**/liste_des_joueurs** pour connaitre la liste des joueurs ainsi que leur numéro.")
    await user.send(embed=msg)

    def check(message):
        return message.author == user and isinstance(message.channel, discord.DMChannel)

    kill = await Bot.wait_for('message', check=check)
    print(kill)
    print(kill.content)
    return kill.content
