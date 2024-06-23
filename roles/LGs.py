import discord
from discord.ext import commands
from Database.databasehandler import DatabaseHandler
from collections import Counter
from checks import check_slash_wait

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot

async def LGs(interaction, Bot):
    users = []
    Lg_list = DatabaseHandler.lg_list()
    votes = []

    for value in Lg_list:
        userid = int(DatabaseHandler.discordID_for_name(value))
        user = await Bot.fetch_user(userid)
        users.append(user)

    for user in users:
        msg = discord.Embed(title="La lune est au plus haut, il est temps pour vous de dévorer un villageois !", colour=0xFF0000)
        msg.add_field(name="info", value="Vote pour une cible en envoyant son numéro.\n**/liste_des_joueurs**")
        await user.send(embed=msg)

    votes = []
    voted_users = set()

    def check(message):
        return (
            message.author.id in [user.id for user in users]
            and isinstance(message.channel, discord.DMChannel)
        )

    while len(voted_users) < len(users):
        voted_message = await Bot.wait_for('message', check=check)

        if voted_message.author.id not in voted_users:
            voted_users.add(voted_message.author.id)
            votes.append(voted_message.content)
            confirmation_msg = discord.Embed(title=f"Tu as voté pour {DatabaseHandler.name_for_number(voted_message.content)} !", colour=0x00FF00)
            await voted_message.author.send(embed=confirmation_msg)

        else:
            msg = discord.Embed(title="Tu ne peux pas voter plusieurs fois pas nuits", colour=0xFF0000)
            await voted_message.author.send(embed=msg)

    counter = Counter(votes)
    killed = counter.most_common(1)[0][0]
    return killed
