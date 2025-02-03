import discord
from discord.ext import commands
import roles.Chasseur as CH
import roles.Voyante as VY
import roles.Cupidon as CP
import roles.LGs as LG
import roles.Sorciere as SC
import roles.Day_votes as DV
from Database.databasehandler import DatabaseHandler
from distribution import SP
import setup as ST
import classNotLoop

DatabaseHandler = DatabaseHandler("database.db")
#Bot = commands.Bot
class win_condition:
    Win_loups = False
    Win_Village = False
    Win_couple = False

class is_alive:
    Sorciere = True
    Voyante = True
    Cupidon = True
    Chasseur = True

async def number_player_list(interaction):
    msg = discord.Embed(title="Liste des joueurs et leur numéro", colour=0xFFFFFF)
    liste = DatabaseHandler.number_list()

    for name, info in liste.items():
        numero, life = info

        if life == 1:
            msg.add_field(name=f"{name} \nen vie", value=f"Numéro : {numero}")
        else:
            msg.add_field(name=f"{name} \nmort", value=f"Numéro : {numero}")

    await interaction.response.send_message(embed=msg, ephemeral=True)


async def start(interaction, bot):
    #if not VD.did_distribution:
       #msg = discord.Embed(title=f"Erreur, la distribution n'est pas faite !", colour=0xFF0000)
       #await interaction.response.send_message(embed=msg)
       #return

    if not ST.variables_setup.Cupidon:
        is_alive.Cupidon = False
    if not ST.variables_setup.Voyante:
        is_alive.Voyante = False
    if not ST.variables_setup.Sorciere:
        is_alive.Sorciere = False
    if not ST.variables_setup.Chasseur:
        is_alive.Chasseur = False

    msg = discord.Embed(title=f"Début de la partie !", colour=0x00FF00)
    await interaction.response.send_message(embed = msg)
    while not win_condition.Win_couple and not win_condition.Win_Village and not win_condition.Win_loups:

        if ST.variables_setup.Cupidon and is_alive.Cupidon:
            if not classNotLoop.one_time_role.Cupidon_played:
                classNotLoop.one_time_role.Cupidon_played = True
                msg = discord.Embed(title=f"Le cupidon joue !")
                await interaction.followup.send(embed=msg, ephemeral=False)
                await CP.Cupidon(interaction, bot)

        if ST.variables_setup.Voyante and is_alive.Voyante:
            msg = discord.Embed(title=f"La voyante observe une personne du village !", colour=0xA71DE1)
            await interaction.followup.send(embed=msg, ephemeral=False)
            await VY.Voyante(interaction, bot)

        killed = []
        Lg_kill = 0
        kill = 0
        if ST.variables_setup.nb_lg > 0:
            lg_msg = discord.Embed(title=f"Les loups vont sortir sous les rayons de la lune", colour=0xFF0000)
            await interaction.followup.send(embed=lg_msg, ephemeral=False)
            Lg_kill = await LG.LGs(interaction, bot)
            kill = 1

        Soso_kill = 0
        if ST.variables_setup.Sorciere and is_alive.Sorciere:
            msg = discord.Embed(title=f"La sorcière va pouvoir faire usage de ses potion !", colour=0xFF8700)
            await interaction.followup.send(embed=msg, ephemeral=False)
            Soso_kill = await SC.Sorciere(interaction, bot, Lg_kill)
            if Soso_kill != 0 and ST.variables_setup.nb_lg > 0:
                kill = 2
                killed.append(Soso_kill)
            elif Soso_kill != 0 and ST.variables_setup.nb_lg <= 0:
                kill = 1
                killed.append(Soso_kill)
            else :
                kill = 0
        if Lg_kill == Soso_kill:
            kill = 1
        killed.append(Lg_kill)
        print(f"kill {kill}")
        for i in range(kill):
            print(f"do_kill/ {killed[i]}")
            await do_kill(interaction, bot, killed[i], False, False)

        if not is_alive.Chasseur and ST.variables_setup.Chasseur:
            if not classNotLoop.one_time_role.chasseur_played:
                classNotLoop.one_time_role.chasseur_played = True
                msg = discord.Embed(title="Comme le chasseur est mort, il peut emporter quelqu'un dans la tombe", colour=0x95D72A)
                await interaction.followup.send(embed=msg)
                chase_kill = await CH.Chasseur(interaction, bot)
                await do_kill(interaction, bot, chase_kill, True, False)

        msg = discord.Embed(title="Le jour se lève !", colour=0x00FF00)
        await interaction.followup.send(embed=msg, ephemeral=False)

        win = await check_win_conditions(interaction)
        if win:
            continue

        msg = discord.Embed(title="Il est l'heure de passer aux votes !", colour=0x00FF00)
        msg.add_field(name="Message privé", value="vous avez reçu un message privé dans lequel vous pouvez voter !")
        await interaction.followup.send(embed=msg, ephemeral=False)

        voted = await DV.votes(interaction, bot)
        print(f"{type(voted)}, {voted}, pk tu crash fdp")

        msg = discord.Embed(title="Les votes sont faits", colour=0x00FF00)
        msg.add_field(name="Le joueur qui va être éliminé est :", value=f"{DatabaseHandler.name_for_number(voted)}")
        await do_kill(interaction, bot, voted, False, True)

        await check_win_conditions(interaction)


async def do_kill(interaction, Bot, number, chase, day):
    infos = DatabaseHandler.death_info(number)
    if chase:
        kill_msg = "à été tué par le chasseur"
    elif day:
        kill_msg = "est le joueur le plus voté, il a donc été pendu"
    else:
        kill_msg = "est mort cette nuit"
    for key, value in infos.items():
        msg = discord.Embed(title=f"{key} {kill_msg}.", colour=0x000000)
        msg.add_field(name=f"Il était", value=f"{value}")
        await interaction.followup.send(embed=msg, ephemeral=False)
        DatabaseHandler.kill_by_name(key)

        if value == f"Cupidon {SP.Cupidon}":
            is_alive.Cupidon = False
        if value == f"Voyante {SP.Voyante}":
            is_alive.Voyante = False
        if value == f"Sorciere {SP.Sorciere}":
            is_alive.Sorciere = False
        if value == f"Chasseur {SP.Chasseur}":
            is_alive.Chasseur = False
        if value == f"Loup-Garou {SP.LG}":
            ST.variables_setup.nb_lg -= 1
        if value == f"Villageois {SP.Villageois}":
            print("enter villager -1")
            ST.variables_setup.nb_villageois -=1


async def check_win_conditions(interaction):
    print(ST.variables_setup.nb_villageois, ST.variables_setup.nb_lg, is_alive.Voyante, is_alive.Sorciere, is_alive.Chasseur, is_alive.Cupidon)
    if ST.variables_setup.nb_villageois == 0 and not is_alive.Voyante and not is_alive.Chasseur and not is_alive.Sorciere and not is_alive.Cupidon:
        win_condition.Win_loups = True

    if ST.variables_setup.nb_lg == 0:
        win_condition.Win_Village = True

    if win_condition.Win_loups and win_condition.Win_Village:
        msg = discord.Embed(title="Fin de la partie !", colour=0x0000FF)
        msg.add_field(name="Egalité", value="aucun camp n'a gagné la partie !")
        await interaction.followup.send(embed=msg, ephemeral=False)
        return True

    if win_condition.Win_Village and not win_condition.Win_loups:
        msg = discord.Embed(title="Fin de la partie !", colour=0x00FF00)
        msg.add_field(name="Victoire du Village !", value="Le village a remporté la partie !")
        await interaction.followup.send(embed=msg, ephemeral=False)
        return True

    if win_condition.Win_loups and not win_condition.Win_Village:
        msg = discord.Embed(title="Fin de la partie !", colour=0xFF0000)
        msg.add_field(name="Victoire des Loups !", value="Les Loups on remporté la partie !")
        await interaction.followup.send(embed=msg, ephemeral=False)
        return True

    return False
