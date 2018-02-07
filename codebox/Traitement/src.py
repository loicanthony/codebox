import sys

def ask_algo():
    """Demande l'algorithme pour l'execution"""
    print(sys.version)
    sys.stdout.write("\nChoisissez l'algorithme"
                     "\n1 pour Coordinate Search de NOMAD (CS)"
                     "\n2 pour Generalized Pattern Search de NOMAD(GPS)"
                     "\n3 pour Mesh Adaptive Direct Search de NOMAD(MADS)"
                     "\n4 pour Generative Set Search de HOPSPACK (GSS)"
                     "\n5 pour Implicit Filtering de imfil (IF)\n")
    while True:
        choice = input().lower()
        if choice == '1':
            sys.stdout.write("1 : CS choisi")
            return 1
        elif choice == '2':
            sys.stdout.write("2 : GPS choisi")
            return 2
        elif choice == '3':
            sys.stdout.write("3 : MADS choisi")
            return 3
        elif choice == '4':
            sys.stdout.write("4 : GSS choisi")
            return 4
        elif choice == '5':
            sys.stdout.write("5 : IF choisi")
            return 5
        else:
            sys.stdout.write("SVP repondre avec 1, 2, 3, 4 ou 5\n")

def ask_strategy(algo):
    """Demande la stratégie pour l'execution"""

    # Les non-dispos sont dans une liste de liste. ex [[1 2][][][4][5]] pour algo 1, strat 1 et 2 sont indisponibles etc.
    dispo = [
        [1, 2, 3, 4, 5, 6, 7],  #cs
        [1, 2, 3, 4, 5, 6, 7], #gps
        [1, 2, 3, 4, 5, 6, 7], #mads
        [2, 3], #hopspack, juste random et determ
        [1, 2, 3, 4, 5, 6, 7] #implicit filtering
    ]
    strategies = ['Sans strategie opportuniste',
                  'Stratégie opportuniste avec ordonnancement deterministe',
                  'Stratégie opportuniste avec ordonnancement aléatoire',
                  'Stratégie opportuniste avec ordonnancement dernier succès',
                  'Stratégie opportuniste avec ordonnancement théorique omniscient',
                  'Stratégie opportuniste avec ordonnancement théorique négatif-omniscient',
                  'Stratégie opportuniste avec ordonnancement avec modeles']

    counter = 1
    corres = []
    sys.stdout.write("\n Choisissez la stratégie pour l'algorithme")
    for x in range(0,len(strategies)):
        if (x+1) in dispo[(algo-1)]:
            sys.stdout.write("\n %s pour %s" % (counter,strategies[x]))
            corres.append((counter,(x+1)))
            counter += 1
    counter -= 1
    sys.stdout.write("\n")
    while True:
        choice = input().lower()
        choice = int(choice)
        if choice <= counter:
            #les objets retournés sont les correspondants au choix dans corres. issue du compteur
            retour = [item[1] for item in corres if item[0] == choice]
            sys.stdout.write("\n%s : %s choisi" % (choice, strategies[(retour[0]-1)]))
            return retour[0]
        else:
            sys.stdout.write("SVP repondre avec un des choix proposes\n")

def main():
    """Démarer la comparaison des algorithmes
    """

    sys.stdout.write("Banc de test pour la comparaison des stratégies d'ordonnancement"
                 "\nChoisissez"
                 "\n1 pour Executer la banque de problème"
                 "\n2 pour Executer une boite noire"
                 "\n3 pour tracer les profils de comparaison d'algorithmes sur CUTEr"
                 "\n4 pour tracer les profils de comparaison d'algorithmes sur l'ensemble des boites noires résolues \n")
    while True:
        choice = input().lower()
        if choice == '1':
            sys.stdout.write("1 : Execution de CUTEr")
            algo = ask_algo()
            strat=ask_strategy(algo)
            #run_cuter(algo,strat)
            return
        elif choice == '2':
            sys.stdout.write("2 : Execution d'une boite noire")
            algo = ask_algo()
            strat = ask_strategy(algo)
            #run_blackbox(algo,strat)
            return
        elif choice == '3':
            sys.stdout.write("3 : Creation des profils avec CUTEst")
            return
        elif choice == '4':
            sys.stdout.write("4 : Execution d'une boite noire")
            return
        else:
            sys.stdout.write("SVP repondre avec 1, 2, 3 ou 4\n")

main()