import discord
import distribution
import roles.Cupidon as CP
import roles.Sorciere as SC
from Database.databasehandler import DatabaseHandler
import setup as ST
import play as PL
import classNotLoop as CNL
import registration as RG

DatabaseHandler = DatabaseHandler("database.db")


async def reset(interaction, new_game : bool):
    msg = discord.Embed(title="Reset en cours", color=0xFF0000)
    if new_game:
        await interaction.followup.send(embed=msg)
    else:
        await interaction.response.send_message(embed=msg)

    CP.voted_player.Cupi_touched = []

    SC.sorciere_var.heal = False
    SC.sorciere_var.kill = False

    distribution.gave_role.Chasseur = False
    distribution.gave_role.Cupidon = False
    distribution.gave_role.Voyante = False
    distribution.gave_role.Sorciere = False
    distribution.variables_distribution.did_distribution = False
    distribution.variables_distribution.player_list = []

    PL.is_alive.Cupidon = True
    PL.is_alive.Voyante = True
    PL.is_alive.Sorciere = True
    PL.is_alive.Chasseur = True
    PL.win_condition.Win_Village = False
    PL.win_condition.Win_loups = False
    PL.win_condition.Win_couple = False

    CNL.one_time_role.Cupidon_played = False
    CNL.one_time_role.Chasseur_played = False

    RG.variables_registration.gived_role = {}
    RG.variables_registration.start = False
    RG.variables_registration.Database = ()
    RG.variables_registration.number_for_player = 1
    RG.variables_registration.end_registration = False
    RG.variables_registration.nb_joueur = 0

    ST.variables_setup.nb_joueurs_fix = 0
    ST.variables_setup.nb_lg = 0
    ST.variables_setup.Cupidon = False
    ST.variables_setup.Chasseur = False
    ST.variables_setup.Sorciere = False
    ST.variables_setup.Voyante = False
    ST.variables_setup.present_role = []

    DatabaseHandler.reset()

    print(new_game)
    msg = discord.Embed(title="Fin du reset", color=0x00FF00)
    if not new_game:
        msg.add_field(name="Nouvelle game ?", value="'/set_game' pour lancer une nouvelle partie", inline=False)
    if new_game:
        msg.add_field(name="Lancement de la configuration de la partie !", value="Tout est prêt.")
    await interaction.followup.send(embed=msg)
