import discord
from discord.ext import commands
import checks
from Database.databasehandler import DatabaseHandler
from distribution import SP
from checks import check_slash_wait

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot


async def Voyante(interaction, Bot):
    allowed_player = DatabaseHandler.name_for_role(f"Voyante {SP.Voyante}")
    userid = int(DatabaseHandler.discordID_for_name(allowed_player))
    user = await Bot.fetch_user(userid)
    msg = discord.Embed(title=f"Quelle joueur veut-tu observer cette nuit ?", colour=0xA71DE1)
    await user.send(embed=msg)
    chosen_one = await Bot.wait_for('message')
    check = False
    check_max = False

    while not check and not check_max:
        chosen_one = await Bot.wait_for('message')
        print(chosen_one.content)
        check = check_slash_wait(chosen_one)
        check_max = checks.check_max_player(chosen_one.content)
    role = DatabaseHandler.role_for_number(chosen_one.content)

    if role == f"Loup-Garou {SP.LG}":
        msg = discord.Embed(title=f"{DatabaseHandler.name_for_number(chosen_one.content)}", colour=0xFF0000)
        msg.add_field(name=f"{role}", value="")
        await user.send(embed=msg)

    else:
        msg = discord.Embed(title=f"{DatabaseHandler.name_for_number(chosen_one.content)}", colour=0x00FF00)
        msg.add_field(name=f"{role}", value="")
        await user.send(embed=msg)