import numpy as npy

def generateStartPoints(file,number):
    # Trouver les bornes des variables

    # Ouvre le fichier
    with open(file, 'r') as f:
        # Ouvrir le parameters.txt
        iniFile = f.readlines()
        f.close()

    # Lire le fichier dans une liste
    table = []  # initialisation de la liste qui contient chaque ligne du fichier
    for x in iniFile:
        # Pour chaque ligne de mon history je dois
        # creer une liste
        # appender la liste a l indice x du array
        ligne = list(map(str, (x.split())))  # creer la ligne de float
        table.append(ligne)  # ajoute a la table

    # Créer les éléments lower et upper bound
    LB = []
    UB = []

    # Trouver la dimension et les bornes
    for ligne in table:
        if ligne and ligne[0] == 'DIMENSION':
            dim = int(ligne[1])
        if ligne and ligne[0] == 'LOWER_BOUND':
            if ligne[1] == '(':  # si les bounds diffèrent
                for x in range(0, dim):
                    # Ajoute les éléments
                    LB.append(float(ligne[(2 + x)]))
            else:
                for x in range(0, dim):  # Sinon on ajoute la meme borne i.e. 3e element de la ligne
                    LB.append(float(ligne[2]))
        if ligne and ligne[0] == 'UPPER_BOUND':
            if ligne[1] == '(':  # si les bounds diffèrent
                for x in range(0, dim):
                    # Ajoute les éléments autres que le premier
                    LB.append(float(ligne[(2 + x)]))
            else:
                for x in range(0, dim):  # Sinon on ajoute la meme borne i.e. 3e element de la ligne
                    UB.append(float(ligne[2]))

    ##Genere n points de départs avec LHCS

    # Variables pour le LHCS
    LB = npy.array(LB)
    UB = npy.array(UB)
    span = UB - LB
    strataSize = span / number

    # Créer la matrice des coordonnées du LHC sans attribution
    unmatched = npy.zeros(dim)  # premier element pour initialiser la matrice
    for x in range(0, number):
        randomArray = npy.random.rand(1, dim)
        unmatched = npy.vstack([unmatched, randomArray * strataSize + x * strataSize])
    unmatched = npy.delete(unmatched, 0, 0)  # enleve le premier element

    # Prends le array des coordonnées non assigné et shuffle les colonnes
    # une a une et reconcatène le tout pour avoir les points du LHC
    listSplit = npy.split(unmatched, dim, 1)
    for colonne in listSplit:
        npy.random.shuffle(colonne)
    matched = npy.array(npy.hstack(listSplit)) + npy.array(LB)
    return matched

