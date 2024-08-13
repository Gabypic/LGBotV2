import discord
from discord.ext import commands
from Database.databasehandler import DatabaseHandler
from collections import Counter
import asyncio

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot

async def votes(interaction, Bot):
    users = []
    player_list = DatabaseHandler.player_list()
    print(f"{users} users at start")

    for value in player_list:
        userid = int(DatabaseHandler.discordID_for_name(value))
        user = await Bot.fetch_user(userid)
        users.append(user)

    votes = []
    voted_users = set()
    print(f"{users} users at set")
    print(f"{voted_users} voted users at set")

    def check(message):
        print(f"{message.author.id} {message.author.name} {message.content}")
        return (
                message.author.id in [user.id for user in users]
                and message.channel.id == interaction.channel.id
        )

    async def wait_for_votes():
        while len(voted_users) < len(users):
            voted_message = await Bot.wait_for('message', check=check)
            print(f"{voted_message.author.id} {voted_message.author.name} {voted_message.content}")
            print(f"{voted_users} voted users at vote")
            if voted_message.author.id not in voted_users:
                voted_users.add(voted_message.author.id)
                votes.append(voted_message.content)
                confirmation_msg = discord.Embed(title=f"{voted_message.author} a voté pour {DatabaseHandler.name_for_number(voted_message.content)} !", colour=0x00FF00)
                await interaction.followup.send(embed=confirmation_msg)

            else:

                msg = discord.Embed(title="Tu ne peux pas voter plusieurs fois", colour=0xFF0000)
                await voted_message.author.send(embed=msg)

    async def time_reminder():
        total_time = 180
        while total_time > 0:
            if total_time == 180 or total_time == 120 or total_time == 60:
                await interaction.channel.send(f"Il te reste {total_time // 60} minute(s) pour voter.")
            elif total_time == 30:
                await interaction.channel.send("Il te reste 30 secondes pour voter !")
            elif total_time == 10:
                await interaction.channel.send("Il te reste 10 secondes pour voter !")

            await asyncio.sleep(10)
            total_time -= 10

    try:
        await asyncio.wait_for(
            asyncio.gather(wait_for_votes(), time_reminder()),
            timeout=180
        )
    except asyncio.TimeoutError:
        pass


    counter = Counter(votes)
    print(f"{counter}, le counter est la oh ")
    killed = counter.most_common(1)[0][0]
    print(f"{type(killed)}, {killed}, pk tu crash fdp")
    return killed
