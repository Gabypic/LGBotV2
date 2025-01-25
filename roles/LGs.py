import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Select
from Database.databasehandler import DatabaseHandler
from collections import Counter

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot


async def LGs(interaction, Bot):
    users = []
    Lg_list = DatabaseHandler.lg_list()
    player_list = DatabaseHandler.alive_player_list()
    votes = []
    has_vote = {"count": 0}
    all_voted = asyncio.Event()

    for value in Lg_list:
        userid = int(DatabaseHandler.discordID_for_name(value))
        if DatabaseHandler.is_alive(userid):
            user = await Bot.fetch_user(userid)
            users.append(user)

    total_users = len(users)

    for user in users:
        msg = discord.Embed(
            title="La lune est au plus haut, il est temps pour vous de dévorer un villageois !",
            colour=0xFF0000
        )
        msg.add_field(
            name="info",
            value="Vote pour une cible en la choisissant dans la liste déroulante."
        )
        options = [discord.SelectOption(label=value) for value in player_list]
        select = Select(placeholder="Choisis un joueur !", options=options)

        async def select_callback(interaction):
            has_vote["count"] += 1
            confirmation_msg = discord.Embed(
                title=f"Tu as voté pour {select.values[0]}:",
                colour=0x00FF00
            )
            print(select.values)
            votes.append(DatabaseHandler.number_for_name(select.values[0]))
            await interaction.response.send_message(embed=confirmation_msg)
            if has_vote["count"] >= total_users:
                all_voted.set()

        select.callback = select_callback

        view = View()
        view.add_item(select)
        await user.send(embed=msg, view=view)

    await all_voted.wait()

    counter = Counter(votes)
    killed = counter.most_common(1)[0][0]
    return killed
