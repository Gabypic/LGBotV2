import discord
from discord.ext import commands
from discord.ui import View, Select
from select import select

from Database.databasehandler import DatabaseHandler
from collections import Counter
import asyncio


DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot


async def votes(interaction, Bot):
    players = []
    player_list = DatabaseHandler.alive_player_list()
    votes = []
    vote_counter = {"count": 0}
    has_vote = []
    all_voted = asyncio.Event()
    votes_complete = False

    for player in player_list:
        userid = int(DatabaseHandler.discordID_for_name(player))
        if DatabaseHandler.is_alive(userid):
            user = await Bot.fetch_user(userid)
            players.append(user)

    total_player = len(players)


    async def wait_for_votes(original_interaction):
        nonlocal votes_complete

        for player in players:
            msg = discord.Embed(
                title="Le jour est venu, il est temps de voter pour éliminer un joueur !",
                colour=discord.Colour.purple()
            )
            msg.add_field(
                name="info",
                value="Vote pour une cible en la choisissant dans la liste déroulante."
            )
            msg.add_field(
                name="Attention",
                value="Une fois que tu as voté, tu ne peux pas revenir en arrière !"
            )
            options = [discord.SelectOption(label=value) for value in player_list]
            select = Select(placeholder="Choisis un joueur !", options=options)

            async def select_callback(interaction):
                if player in has_vote:
                    already_voted_msg = discord.Embed(
                        title="Tu ne peut pas voter plusieurs fois !",
                        colour=0xFF0000
                    )
                    await interaction.followup.send(embed=already_voted_msg)
                    return
                vote_counter["count"] += 1
                has_vote.append(player)
                confirmation_msg = discord.Embed(
                    title=f"Tu as voté pour {select.values[0]}:",
                    colour=0x00FF00
                )
                votes.append(DatabaseHandler.number_for_name(select.values[0]))
                await interaction.response.send_message(embed=confirmation_msg)
                general_msg = discord.Embed(
                    title=f"{player} à voté pour {select.values[0]}",
                    colour=discord.Colour.purple()
                )
                original_interaction.followup.send(embed=general_msg)
                if vote_counter["count"] >= total_player:
                    all_voted.set()

            select.callback = select_callback
            view = View()
            view.add_item(select)
            await player.send(embed=msg, view=view)

        await all_voted.wait()
        votes_complete = True

    async def time_reminder():
        total_time = 180
        while total_time > 0:
            if votes_complete:
                break

            if total_time == 180 or total_time == 120 or total_time == 60:
                await interaction.channel.send(f"Il reste {total_time // 60} minutes pour voter.")
            elif total_time == 30:
                await interaction.channel.send("Il reste 30 secondes pour voter !")
            elif total_time == 10:
                await interaction.channel.send("Il reste 10 secondes pour voter !")

            await asyncio.sleep(2)
            total_time -= 2

    try:
        await asyncio.wait_for(
            asyncio.gather(wait_for_votes(interaction), time_reminder()),
            timeout=180
        )
    except asyncio.TimeoutError:
        pass

    counter = Counter(votes)
    killed = counter.most_common(1)[0][0]
    return killed
