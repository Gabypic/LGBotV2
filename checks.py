from setup import variables_setup as VS

def check_slash_wait(to_check):
    try:
        int(to_check.content)
        return True
    except:
        return False


def check_max_player(choice):
    try:
        choice_int = int(choice)
        max_players = int(VS.nb_joueurs_fix)
        return choice_int <= max_players
    except ValueError:  # Si 'choice' ou 'VS.nb_joueurs_fix' ne peut pas être converti en int
        print("L'entrée doit être un nombre.")
        return False
