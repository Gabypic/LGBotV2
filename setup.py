import discord
from discord.ext import commands

class variables_setup:
    Bot = commands.Bot
    nb_joueurs = int
    nb_joueurs_fix = 0
    nb_villageois = int
    nb_lg = 0
    Sorciere = False
    Cupidon = False
    Voyante = False
    Chasseur = False
    game_setup = bool
    present_role = []

class config_buttons(discord.ui.View):
    @discord.ui.button(label="Valider ✅", style=discord.ButtonStyle.success)
    async def valide_button(self,interaction: discord.Interaction, button: discord.ui.Button):
        msg = discord.Embed(title=f"Début de la configuration", colour=0x00FF00)
        await interaction.response.send_message(embed=msg)
        await rolesChoice(interaction)

    @discord.ui.button(label="Annuler ❌", style=discord.ButtonStyle.danger)
    async def unvalid_button(self,interaction: discord.Interaction, button: discord.ui.Button):
        msg = discord.Embed(title="La partie a été annulée !", colour=0xFF0000)
        await interaction.response.send_message(embed=msg)

class roles_button(discord.ui.View):
    @discord.ui.button(label="🧙‍♀️ Sorcière", style=discord.ButtonStyle.grey)
    async def soso_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg = discord.Embed(title=f"La Sorcière est ajoutée", colour=0x00FF00)
        await interaction.response.send_message(embed=msg)
        variables_setup.Sorciere = True
        variables_setup.nb_joueurs -= 1
        variables_setup.present_role.append("Sorciere")

    @discord.ui.button(label="💘 Cupidon", style=discord.ButtonStyle.grey)
    async def cupi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg = discord.Embed(title=f"Le Cupidon est ajouté", colour=0x00FF00)
        await interaction.response.send_message(embed=msg)
        variables_setup.Cupidon = True
        variables_setup.nb_joueurs -= 1
        variables_setup.present_role.append("Cupidon")

    @discord.ui.button(label="🔮 Voyante", style=discord.ButtonStyle.grey)
    async def vovo_button(self, interaction: discord.Interaction, button: discord.ui.button()):
        msg = discord.Embed(title=f"La voyante est ajouté", colour=0x00FF00)
        await interaction.response.send_message(embed=msg)
        variables_setup.Voyante = True
        variables_setup.nb_joueurs -= 1
        variables_setup.present_role.append("Voyante")

    @discord.ui.button(label="🏹 Chasseur", style=discord.ButtonStyle.grey)
    async def chasseur_button(self, interaction: discord.Interaction, button: discord.ui.button()):
        msg = discord.Embed(title=f"Le Chasseur est ajouté", colour=0x00FF00)
        await interaction.response.send_message(embed=msg)
        variables_setup.Chasseur = True
        variables_setup.nb_joueurs -= 1
        variables_setup.present_role.append("Chasseur")

    @discord.ui.button(label="valider ✅", style=discord.ButtonStyle.success)
    async def val_button(self, interaction: discord.Interaction, button: discord.ui.button()):
        msg = discord.Embed(title=f"Les rôles sont fait", colour=0x00FF00)
        msg.add_field(name="Passont aux nombre de loups", value="Tu va pouvoir choisir le nombre de loups")
        await interaction.response.send_message(embed=msg)
        await nb_loups(interaction)

    @discord.ui.button(label="🧙‍♀️ Sorcière", style=discord.ButtonStyle.danger)
    async def del_soso_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg = discord.Embed(title=f"La Sorcière a été retirée", colour=0xFF0000)
        await interaction.response.send_message(embed=msg)
        variables_setup.Sorciere = False
        variables_setup.nb_joueurs += 1
        variables_setup.present_role.remove("Sorciere")

    @discord.ui.button(label="💘 Cupidon", style=discord.ButtonStyle.danger)
    async def del_cupi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg = discord.Embed(title=f"Le Cupidon a été retiré", colour=0xFF0000)
        await interaction.response.send_message(embed=msg)
        variables_setup.Cupidon = False
        variables_setup.nb_joueurs += 1
        variables_setup.present_role.remove("Cupidon")

    @discord.ui.button(label="🔮 Voyante", style=discord.ButtonStyle.danger)
    async def del_vovo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg = discord.Embed(title=f"La Voyante a été retirée", colour=0xFF0000)
        await interaction.response.send_message(embed=msg)
        variables_setup.Voyante = False
        variables_setup.nb_joueurs += 1
        variables_setup.present_role.remove("Voyante")

    @discord.ui.button(label="🏹 Chasseur", style=discord.ButtonStyle.danger)
    async def del_chasseur_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg = discord.Embed(title=f"Le Chasseur a été retiré", colour=0xFF0000)
        await interaction.response.send_message(embed=msg)
        variables_setup.Chasseur = False
        variables_setup.nb_joueurs += 1
        variables_setup.present_role.remove("Chasseur")

async def Setup(interaction, number: int, Bot):
    vue_config = config_buttons()
    variables_setup.nb_joueurs = number
    variables_setup.nb_joueurs_fix = number
    print(variables_setup.nb_joueurs_fix, type(variables_setup.nb_joueurs_fix))
    variables_setup.Bot = Bot
    msg = discord.Embed(title=f"Le jeu sera configuré pour {number} joueurs ", colour=0x0000FF)
    msg.add_field(name="Validation", value=f"Appuyez sur le bouton ✅ pour valider ou ❌ pour annuler")
    await interaction.response.send_message(embed=msg, ephemeral=False, view=vue_config)

async def rolesChoice(interaction):
    global nombre_de_joueurs
    msg = discord.Embed(title=f"Choix des rôles", colour=0x00FF00)
    msg.add_field(name="Choisis les rôles que tu veux dans la partie !", value="Trouve l'équilibre parfait !")
    vue_roles = roles_button()
    message_roles = await interaction.followup.send( embed=msg, ephemeral=False,view=vue_roles)

async def nb_loups(interaction):
    msg = discord.Embed(title="Nombre de Loups <:loupgarou:1075445518827798599>", colour=0x00FF00)
    msg.add_field(name=f"",value=f"Envoie le nombre de loups-garous que tu souhaite dans la partie !")
    await interaction.followup.send(embed=msg)
    def check_lg(message):
        return message.author == interaction.user and message.channel == interaction.message.channel

    nb_lg = await variables_setup.Bot.wait_for('message', check=check_lg)
    variables_setup.nb_lg = int(nb_lg.content)
    variables_setup.nb_villageois = int(variables_setup.nb_joueurs) - int(nb_lg.content)
    await recap(interaction)

async def recap(interaction):
    msg = discord.Embed(title="Récapitulatif Game", colour=0x00FF00)
    msg.add_field(name=f"Loups <:loupgarou:1075445518827798599>", value=f"{variables_setup.nb_lg} loups")
    msg.add_field(name=f"Villageois <:villageois:1075445510682464306>", value=f"{variables_setup.nb_villageois} villageois")

    if variables_setup.Sorciere:
        msg.add_field(name="Sorcière <:sorciere:1075444286667116635>", value="✅")
    else:
        msg.add_field(name="Sorcière <:sorciere:1075444286667116635>", value="❌")

    if variables_setup.Cupidon:
        msg.add_field(name="Cupidon <:cupidon:1075445537114951690>", value="✅")
    else:
        msg.add_field(name="Cupidon <:cupidon:1075445537114951690>", value="❌")

    if variables_setup.Voyante:
        msg.add_field(name="Voyante <:voyante:1075445527107342426>", value="✅")
    else:
        msg.add_field(name="Voyante <:voyante:1075445527107342426>", value="❌")

    if variables_setup.Chasseur:
        msg.add_field(name="Chasseur <:chasseur:1075445480265351178>", value="✅")
    else:
        msg.add_field(name="Chasseur <:chasseur:1075445480265351178>", value="❌")

    await interaction.followup.send(embed=msg)
    variables_setup.game_setup = True
