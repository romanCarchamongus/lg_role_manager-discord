import random as r

def getCompo(nbPlayer):
    roles = []
    for i in range(nbPlayer):
        roles.append(input("Role :\n"))
    return roles

def getPlayers(nbPlayer):
    players = []
    for i in range(nbPlayer):
        players.append(input("Player :\n"))
    return players

def assignRoles(roles, players):
    d = {}
    for p in players:
        d[p]=roles.pop(r.randint(0,len(roles)-1))
    return d

def initRoleDistribution(nbPlayer):
    d = assignRoles(getCompo(nbPlayer),getPlayers(nbPlayer))
    for k in d.keys():
        print(f"Joueur {k} => {d[k]}")

if __name__ == '__main__':
    initRoleDistribution(5)