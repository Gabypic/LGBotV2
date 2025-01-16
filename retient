import discord
from discord.ext import commands
from Database.databasehandler import DatabaseHandler
from collections import Counter
import asyncio
import checks

DatabaseHandler = DatabaseHandler("database.db")
Bot = commands.Bot


async def votes(interaction, Bot):
    users = []
    player_list = DatabaseHandler.player_list()

    for value in player_list:
        userid = int(DatabaseHandler.discordID_for_name(value))
        vivant = DatabaseHandler.is_alive(userid)
        if vivant:
            user = await Bot.fetch_user(userid)
            users.append(user)

    votes = []
    voted_users = []
    votes_complete = False  # Variable de contrôle

    print(f"{users} le users \n {len(users)} le len la")

    def check(message):
        print(f"{message.author.id} {message.author.name} {message.content}")
        return (
                message.author.id in [user.id for user in users]
                and message.channel.id == interaction.channel.id
        )

    async def wait_for_votes():
        nonlocal votes_complete  # Permet de modifier la variable dans la portée extérieure
        while len(voted_users) < len(users):
            print("waiting for votes")
            print(f"{len(voted_users)} voted users, {len(users)} users")
            voted_message = await Bot.wait_for('message', check=check)
            print(f"{voted_message.author.id} {voted_message.author.name} {voted_message.content} aaaaaaaaaaah")
            check_number = checks.check_slash_wait(voted_message)
            check_max = checks.check_max_player(voted_message.content)
            print(f"{check_number} number {check_max} max")

            if (voted_message.author.id not in voted_users and DatabaseHandler.is_alive(voted_message.author.id)
                    and check_number and check_max):
                voted_users.append(voted_message.author.id)
                votes.append(voted_message.content)
                confirmation_msg = discord.Embed(title=f"{voted_message.author} a voté pour "
                                                       f"{DatabaseHandler.name_for_number(voted_message.content)} !",
                                                 colour=0x00FF00)
                await interaction.followup.send(embed=confirmation_msg)

            else:
                if not check_max and DatabaseHandler.is_alive(voted_message.author.id) and check_number:
                    msg = discord.Embed(title="Le numéro que tu as envoyé n'appartient à aucun joueur", colour=0xFF0000)
                    await voted_message.author.send(embed=msg)
                elif not check_number and DatabaseHandler.is_alive(voted_message.author.id):
                    msg = discord.Embed(title="Il faut voter par le numéro du joueur", colour=0xFF0000)
                    msg.add_field(name="Il ne doit contenir que le numéro", value="")
                    await voted_message.author.send(embed=msg)
                elif not DatabaseHandler.is_alive(voted_message.author.id):
                    msg = discord.Embed(title="Tu ne peux pas voter en étant mort", colour=0xFF0000)
                    await voted_message.author.send(embed=msg)
                else:
                    msg = discord.Embed(title="Tu ne peux pas voter plusieurs fois", colour=0xFF0000)
                    await voted_message.author.send(embed=msg)

        votes_complete = True  # Tous les votes sont terminés
        print(votes_complete, "salut")

    async def time_reminder():
        total_time = 180
        while total_time > 0:
            if votes_complete:  # Arrête la boucle si les votes sont terminés
                break

            if total_time == 180 or total_time == 120 or total_time == 60:
                await interaction.channel.send(f"Il te reste {total_time // 60} minutes pour voter.")
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
    killed = counter.most_common(1)[0][0]
    return killed
