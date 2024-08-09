import discord
from discord.ext import commands
from setup import variables_setup as VS
from registration import variables_registration
from Database.databasehandler import DatabaseHandler
import random

DatabaseHandler = DatabaseHandler("database.db")

class SP:
    Sorciere = "<:sorciere:1075444286667116635>"
    Cupidon = "<:cupidon:1075445537114951690>"
    LG = "<:loupgarou:1075445518827798599>"
    Voyante = "<:voyante:1075445527107342426>"
    Chasseur = "<:chasseur:1075445480265351178>"
    Villageois = "<:villageois:1075445510682464306>"

class gave_role:
    Sorciere = False
    Cupidon = False
    Voyante = False
    Chasseur = False

class variables_distribution:
    player_list = []
    did_distribution = False

async def Distribution(interaction):
    if not variables_registration.end_registration:
        msg = discord.Embed(title=f"Erreur, le inscriptions ne sont pas terminée !", colour=0xFF0000)
        await interaction.response.send_message(embed=msg)
        return
    msg = discord.Embed(title="Début de la distribution des rôles !", colour=0x00FF00)
    await interaction.response.send_message(embed=msg)
    take_player_list = DatabaseHandler.player_list()
    variables_distribution.player_list = take_player_list
    nb_lg = VS.nb_lg
    nb_villageois = VS.nb_villageois
    if VS.Voyante and not gave_role.Voyante and len(take_player_list) != 0:
        random_player = random.randint(0,len(take_player_list)-1)
        DatabaseHandler.add_player_role(take_player_list[random_player], f"Voyante {SP.Voyante}")
        gave_role.Voyante = True
        take_player_list.remove(take_player_list[random_player])

    if VS.Cupidon and not gave_role.Cupidon and len(take_player_list) != 0:
        random_player = random.randint(0, len(take_player_list)-1)
        DatabaseHandler.add_player_role(take_player_list[random_player], f"Cupidon {SP.Cupidon}")
        gave_role.Cupidon = True
        take_player_list.remove(take_player_list[random_player])

    if VS.Chasseur and not gave_role.Chasseur and len(take_player_list) != 0:
        random_player = random.randint(0, len(take_player_list)-1)
        DatabaseHandler.add_player_role(take_player_list[random_player], f"Chasseur {SP.Chasseur}")
        gave_role.Chasseur = True
        take_player_list.remove(take_player_list[random_player])

    if VS.Sorciere and not gave_role.Sorciere and len(take_player_list) != 0:
        random_player = random.randint(0, len(take_player_list)-1)
        DatabaseHandler.add_player_role(take_player_list[random_player], f"Sorciere {SP.Sorciere}")
        gave_role.Voyante = True
        take_player_list.remove(take_player_list[random_player])

    while nb_lg != 0:
        if len(take_player_list) != 0:
            random_player = random.randint(0, len(take_player_list)-1)
            DatabaseHandler.add_player_role(take_player_list[random_player], f"Loup-Garou {SP.LG}")
            nb_lg -= 1
            take_player_list.remove(take_player_list[random_player])
        else:
            continue

    while nb_villageois != 0:
        if len(take_player_list) != 0:
            random_player = random.randint(0, len(take_player_list)-1)
            DatabaseHandler.add_player_role(take_player_list[random_player], f"Villageois {SP.Villageois}")
            nb_villageois -= 1
            take_player_list.remove(take_player_list[random_player])
        else:
            continue

    msg = discord.Embed(title="Fin de la distribution des rôles", colour=0x00FF00)
    msg.add_field(name="Information :", value=f"**/me** pour voir ton rôle !")
    await interaction.followup.send(embed=msg)
    variables_distribution.did_distribution =True


async def me(interaction, name : str):
    role = DatabaseHandler.role_for_name(str(name))
    if role == f"Loup-Garou {SP.LG}":
        msg = discord.Embed(title="Role", colour=0xFF0000)
        msg.add_field(name="Ton rôle est :", value=f"{role}")
        await interaction.response.send_message(embed=msg, ephemeral=True)

    elif role == f"Villageois {SP.Villageois}" :
        msg = discord.Embed(title="Role", colour=0xFEF96F)
        msg.add_field(name="Ton rôle est :", value=f"{role}")
        await interaction.response.send_message(embed=msg, ephemeral=True)

    elif role == f"Sorciere {SP.Sorciere}":
        msg = discord.Embed(title="Role", colour=0xC87C00)
        msg.add_field(name="Ton rôle est :", value=f"{role}")
        await interaction.response.send_message(embed=msg, ephemeral=True)

    elif role == f"Chasseur {SP.Chasseur}":
        msg = discord.Embed(title="Role", colour=0x51B800)
        msg.add_field(name="Ton rôle est :", value=f"{role}")
        await interaction.response.send_message(embed=msg, ephemeral=True)

    elif role == f"Cupidon {SP.Cupidon}":
        msg = discord.Embed(title="Role", colour=0x00AAFF)
        msg.add_field(name="Ton rôle est :", value=f"{role}")
        await interaction.response.send_message(embed=msg, ephemeral=True)

    elif role == f"Voyante {SP.Voyante}":
        msg = discord.Embed(title="Role", colour=0xB600FF)
        msg.add_field(name="Ton rôle est :", value=f"{role}")
        await interaction.response.send_message(embed=msg, ephemeral=True)
