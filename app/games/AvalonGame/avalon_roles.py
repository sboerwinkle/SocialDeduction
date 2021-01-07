import csv
import random


# global defined roles
roles = {
    # Good characters
    "Merlin" : {
        "Name": "Merlin",
        "Team": "Good",
        "Number": 1
    },
    "Percival" : {
        "Name": "Percival",
        "Team": "Good",
        "Number": 1
    },
    "Loyal Servant of Arthur" : {
        "Name": "Loyal Servant of Arthur",
        "Team": "Good",
        "Number": 4
    },

    # Evil characters separator
    "Mordred" : {
        "Name": "Mordred",
        "Team": "Evil",
        "Number": 1
    },
    "Morgana" : {
        "Name": "Morgana",
        "Team": "Evil",
        "Number": 1
    },
    "Assassin" : {
        "Name": "Assassin",
        "Team": "Evil",
        "Number": 1
    },
    "Oberon" : {
        "Name": "Oberon",
        "Team": "Evil",
        "Number": 1
    },
    "Minion of Mordred" : {
        "Name": "Minion of Mordred",
        "Team": "Evil",
        "Number": 3
    },
}


# global defined
def get_role_knowledge(role, role_dict_unshuffled):
    global roles
    out_str = ""

    # Shuffles roles
    active_roles = list(role_dict_unshuffled.keys())
    random.shuffle(active_roles)

    # only use this dict, otherwise metagaming.
    role_to_player = {x: role_dict_unshuffled[x] for x in active_roles}
    # this prevents metagaming through the fact that roles are always displayed same order.

    # evil Team
    if roles[role].team == "Evil":
        if role == "Oberon":
            return "I'm here to chew ass and kick bubblegum. And I'm all out of bubblegum."


        # minus oberon, of course
        evil_players = []
        for p_role, player in role_to_player.items():
            if roles[p_role].team == "Evil" and p_role != "Oberon" and p_role != role:
                evil_players.append(player)
        random.shuffle(evil_players)

        out_str += "You know that <br> " + ', '.join(evil_players) + "</br> are your evil compatriots."

        if "Oberon" in active_roles:
            out_str += "\nHowever, Oberon is unknown to you..."


        return out_str

    # merlin knows all evil except mordred
    if role == "Merlin":
        out_str = "You are Merlin. You know that <br> "

        for p_role, player in role_to_player.items():
            if roles[p_role].team == "Evil" and p_role != "Mordred":
                out_str += player
                out_str += ", "

            # remove trailing seperator
            out_str = out_str[:-2]
            out_str += "</br> belong to Evil and are working against you."

            if "Mordred" in active_roles:
                out_str += "\nHowever, Mordred is still unknown to you..."

    # Percival knows merlin and morgana, but not which is which.
    elif role == "Percival":
        if "Merlin" in active_roles and "Morgana" in active_roles:
            per_roles = [role_to_player["Merlin"], role_to_player["Morgana"]]
            random.shuffle(per_roles)

            out_str = "You know that <br>" + per_roles[0] + ", " + per_roles[1] + "</br> are Merlin and Morgana."
            out_str += "\nHowever, you do NOT know which is which!." 

        elif "Merlin" in active_roles:
            out_str = "You know that <br>" + role_to_player["Merlin"] + "</br> is Merlin."
        elif "Morgana" in active_roles:
            out_str = "You know that <br>" + role_to_player["Morgana"] + "</br> is Morgana."

    # Loyal servants know nothing.
    elif role == "Loyal Servant of Arthur":
        out_str = "May Arthur and the good team prevail!"
    

    return out_str



def get_knowledge_text(assigned_roles, players):
    """
        Expects assigned roles to be a dict
        of player ID to role.
    """
    global roles

    roleplayer_dict = {v: players[k].name for k, v in assigned_roles.items()}



def get_roles():
    global roles
    return roles





# def get_roles(filename="avalon_roles.csv"):
#     roles = {}

#     with open(filename) as csvfile:
#         rolesfile = csv.reader(csvfile, delimiter=",")
#         for row in rolesfile:
#             if row[0] == "Name":
#                 continue

#             role_info = {
#                 "Name": row[0],
#                 "Team": row[1],
#                 "Number": int(row[2]),
#                 "Knowledge": row[3]
#             }
            
#             roles[row[0]] = role_info
#     return roles
