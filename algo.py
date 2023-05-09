text = open("nodes.txt")
dico = {}
for line in text:
    dico[eval(line.split("\t")[0])] = eval(line.split("\t")[3])

def dijktra(sommet, arriver):
    tableau = {}
    T = []
    for i in range(2, len(dico)+2):
        tableau[i] = ("-", 999999)
    tableau[sommet] = (None, 0)
    for noeud, nom, type, distance in dico[sommet]:
        tableau[noeud] = (sommet, distance)
    T.append(sommet)
    return chemin_plus_court(sommet, arriver, dijktra_main(tableau, T))

def dijktra_main(tableau, T):
    while len(T) < len(tableau):
        try:
            print(len(T), len(tableau))
            mini = 999999
            sommet = None
            for noeud, (pere, distance) in tableau.items():
                if noeud not in T:
                    if distance < mini:
                        mini = distance
                        sommet = noeud
            for noeud, nom, type, distance in dico[sommet]:
                if tableau[sommet][1]+distance < tableau[noeud][1]:
                    tableau[noeud] = (sommet, tableau[sommet][1]+distance)
            T.append(sommet)
        except KeyError:
            break
    return tableau

def chemin_plus_court(depart, arriver, tableau):
    chemin = []
    noeud = arriver
    while noeud != None:
        chemin.insert(0, noeud)
        noeud = tableau[noeud][0]
    return chemin

print(dijktra(78, 130))
