import discord
from discord.ext import commands
from setup import variables_setup
from Database.databasehandler import DatabaseHandler

DatabaseHandler = DatabaseHandler("database.db")
class variables_registration:
    Bot = variables_setup.Bot
    gived_role = {}
    start = False
    Database = ()
    number_for_player = 1
    end_registration = False
    nb_joueur = 0


async def Start_Inscriptions(interaction, name, user_id, database):
    if variables_setup.game_setup == True:
        variables_registration.Database = database
        msg = discord.Embed(title="Début des inscriptions", colour=0x00FF00)
        msg.add_field(name="Inscrivez-vous !", value="@everyone")
        await interaction.response.send_message(embed=msg)
        variables_registration.start = True
        variables_registration.nb_joueur = variables_setup.nb_joueurs_fix
        print(variables_registration.nb_joueur)
    else :
        msg = discord.Embed(title="Erreur", colour=0xFF0000)
        msg.add_field(name="La game n'est pas Setup", value="*/set_game* pour configurer la game")
        await interaction.response.send_message(embed=msg)

async def Inscription(interaction, name, user_id):
    if variables_registration.start and variables_setup.game_setup and not DatabaseHandler.no_player(name) and variables_registration.nb_joueur != 0:
        variables_registration.nb_joueur -= 1
        msg = discord.Embed(title="Joueur inscrit !", colour=0x0000FF)

        if variables_registration.nb_joueur <= 2:
            msg.add_field(name="Information", value=f"Il ne reste plus que {variables_registration.nb_joueur} places")

        await interaction.response.send_message(embed=msg)
        DatabaseHandler.add_player(name, user_id, variables_registration.number_for_player, 0)
        variables_registration.number_for_player += 1

    elif DatabaseHandler.no_player(name):
        msg = discord.Embed(title="Joueur déjà inscrit !", colour=0xFF0000)
        msg.add_field(name="Tu es déjà inscrit !", value="Tu ne peux pas t'inscrire deux fois !")
        await interaction.response.send_message(embed=msg, ephemeral=True)

    elif not variables_registration.start:
        msg = discord.Embed(title="Les inscriptions n'ont pas encore commencé !", colour=0xFF0000)
        msg.add_field(name="Attend l'annonce du game master pour pouvoir t'inscrire.", value="")
        await interaction.response.send_message(embed=msg, ephemeral=True)

    if variables_registration.end_registration:
        msg = discord.Embed(title="Tu ne peux plus t'inscrire !", colour=0xFF0000)
        msg.add_field(name="Les inscriptions sont clôturée.", value=f"Attend la prochaine partie !")
        await interaction.response.send_message(embed=msg)

    if variables_registration.nb_joueur == 0 and variables_registration.start and not variables_registration.end_registration:
        msg = discord.Embed(title=f"Fin des inscriptions", colour=0x0000FF)
        await interaction.followup.send(embed=msg)
        variables_registration.end_registration = True
