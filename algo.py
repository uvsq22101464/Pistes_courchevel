text = open("nodes.txt")
dico = {}
for line in text:
    dico[eval(line.split("\t")[0])] = eval(line.split("\t")[3])

dico_niveau = {"Débutant" : {"green" : 1.2, "blue" : 1.8, "red" : 2.5, "black" : 4},
            "Aguerri" : {"green" : 1.1, "blue" : 1.4, "red" : 1.8, "black" : 2.5},
            "Expert" : {"green" : 1, "blue" : 0.9, "red" : 0.8, "black" : 0.6}}

dico_remonte = {"teleski" : 2, "telesiege" : 1.7, "telecabine" : 1.4, "telepherique" : 1.1} 

def dijktra(sommet, arriver,niveau):
    tableau = {}
    T = []
    for i in range(2, len(dico)+2):
        tableau[i] = ("-", 999999)
    tableau[sommet] = (None, 0)
    for noeud, nom, type, distance in dico[sommet]:
        tableau[noeud] = (sommet, distance)
    T.append(sommet)
    liste_chemin = chemin_plus_court(sommet, arriver, dijktra_main(tableau, T,niveau))
    nom_chemin = []
    for i in range(len(liste_chemin)-1):
        for noeud, nom, type, distance in dico[liste_chemin[i]]:
            if noeud == liste_chemin[i+1]:
                nom_chemin.append(nom)
    return liste_chemin, nom_chemin

def dijktra_main(tableau, T,niveau):
    while len(T) < len(tableau):
        mini = 999999
        sommet = None
        for noeud, (pere, distance) in tableau.items():
            if noeud not in T:
                if distance < mini:
                    mini = distance
                    sommet = noeud
        if sommet is not None:
            if  sommet != '-':
                for noeud, nom, type, distance in dico[sommet]:
                    if type != "telecabine" and type != "teleski" and type != "telesiege" and type != "telepherique":
                        if tableau[sommet][1]+distance * dico_niveau[niveau][type] < tableau[noeud][1]:
                            tableau[noeud] = (sommet, tableau[sommet][1]+distance* dico_niveau[niveau][type])
                    else:
                        if tableau[sommet][1]+distance * dico_remonte[type] < tableau[noeud][1]:
                            tableau[noeud] = (sommet, tableau[sommet][1]+distance* dico_remonte[type])
                T.append(sommet)
        else:
            break
    return tableau

def chemin_plus_court(depart, arriver, tableau):
    chemin = []
    noeud = arriver
    if tableau[noeud][0] == '-':
        return chemin
    while noeud != None:
        chemin.insert(0, noeud)
        noeud = tableau[noeud][0]
    return chemin
