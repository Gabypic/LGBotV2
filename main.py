#####################
# LG_BotV2          #
# Version Alpha 0.9 #
# Créé : 03/10/2023 #
# Par : Gabychouuu_ #
# maj : 13/08/2024  #
#####################

import discord
from discord.ext import commands
import play
import setup
import registration
import distribution
import reset
from Database.databasehandler import DatabaseHandler
from setup import variables_setup as st
from registration import variables_registration as rg

DatabaseHandler = DatabaseHandler("database.db")
intents = discord.Intents.all()
Bot = commands.Bot(command_prefix="!", description="Go pour les LGs", intents=intents)
discord.AllowedMentions(everyone=True, users=True, roles=True, replied_user=True)
version = "Alpha 0.9"

@Bot.event
async def on_ready():
    global version
    log_channel = Bot.get_channel(1042913689491226757)
    msg = discord.Embed(title=f"Démarrage", colour=discord.Colour(0x00FF00))
    msg.add_field(name="vesrion :", value=f"{version}")
    try:
       synced = await Bot.tree.sync()
       print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    await log_channel.send(embed=msg)

@Bot.tree.command()
async def set_game(interaction, number : int):
    try:
        global Bot
        bot = Bot
        msg = discord.Embed(title="Reset avant setup", colour=0x0000FF)
        await interaction.response.send_message(embed=msg)
        await reset.reset(interaction, True)
        await setup.Setup(interaction, number, bot)
    except Exception as e:
        msg = discord.Embed(title="La préparation de la game a crash", colour=discord.Colour(0xFF0000))
        msg.add_field(name="Erreur : ", value=str(e))
        await interaction.followup.send(embed=msg)
        print(f"crash report {e}")

@Bot.tree.command()
async def start_inscriptions(interaction):
    try:
        name = interaction.user
        user_id = int(interaction.user.id)
        await registration.Start_Inscriptions(interaction, name, user_id, DatabaseHandler)
    except Exception as e:
        msg = discord.Embed(title="Le début des inscriptions a crash", colour=discord.Colour(0xFF0000))
        msg.add_field(name="Erreur : ", value=str(e))
        await interaction.followup.send(embed=msg)
        print(f"crash report {e}")

@Bot.tree.command()
async def inscription(interaction):
    user = interaction.user
    user_id = user.id
    name = str(user)
    await registration.Inscription(interaction, name, user_id)

@Bot.tree.command()
async def distribution_roles(interaction):
    try:
        await distribution.Distribution(interaction)
    except Exception as e:
        msg = discord.Embed(title="La distribution a crash", colour=discord.Colour(0xFF0000))
        msg.add_field(name="Erreur : ", value=str(e))
        await interaction.followup.send(embed=msg)
        print(f"crash report {e}")

@Bot.tree.command()
async def me(interaction):
    name = interaction.user
    await distribution.me(interaction, name)

@Bot.tree.command()
async def liste_des_joueurs(interaction):
    await play.number_player_list(interaction)

@Bot.tree.command()
async def start(interaction):
    #try :
        global Bot
        bot = Bot
        await play.start(interaction, bot)
    #except Exception as e:
    #    msg = discord.Embed(title="La game à crash", colour=discord.Colour(0xFF0000))
    #    msg.add_field(name="Erreur : ", value=str(e))
    #    await interaction.followup.send(embed=msg)
    #    print(f"crash report {e}")


@Bot.tree.command()
async def reset_game_settings(interaction):
    await reset.reset(interaction, False)

Bot.run("MTA0MjkxMjk4Njc3MzMyNzkyMw.GhkAnU.4mQRT_wRgA_Go0ygpETT7zdqHc4haXG1KgCNVY")