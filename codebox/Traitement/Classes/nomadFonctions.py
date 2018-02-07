import matplotlib.pyplot as plt
import Classes.History as History
import numpy as npy
import random

def readLog_singleprob(path):
    # Reader de log de NOMAD et creer un objet history consequent

    # Regarde par le nom les specs de la run
    file = path.split('\\')[-1]
    name = file.split('_')
    ext = name[-1].split('.')[-1]
    name[-1]=name[-1].split('.')[0]
    name.append(ext)

    #Erreur si on a pas un file history
    if name[2]!='history':
        print('file provided is not of the right format')
        return

    #On cree un objet history
    history=History.History()

    #Nom, Classe, solveur et parametre#  de resolution du probleme
    history.setProblem(str(name[0]))
    history.setStartpoint(str(name[1]))
    history.setSeed(str(name[3]))
    history.setAlgo(str(name[4][0]))
    history.setStrat(str(name[4][1:]))
    history.setSolver('NOMAD')

    # Ouvrir le history.txt
    with open(path, 'r') as file:
        iniFile = file.readlines()
        file.close()

    # Mettre la history dans l'objet
    nbIteration = len(iniFile) #nombre de lignes dans le fichier
    table = []  # initialisation de ma liste
    for x in range(0, nbIteration):
        # Pour chaque ligne de mon history je dois
        # creer une liste
        # appender la liste a l indice x du array
        ligne = list(map(float, (iniFile[x]).split()))  # creer la ligne de float
        table.append(ligne)  # ajoute a la table
    history.setTable(table)

    # Determiner la dimension du probleme
    # Inutile je crois, on a juste a prendre la derniere valeur

    # paramPath = path[:-(len(path.split('\\')[-1]))]
    # paramName = history.getSeed()+'_param.txt'
    # paramFile = paramPath+paramName
    # with open(paramFile, 'r') as f:
    #     # Ouvrir le parameters.txt
    #     params = f.readlines()
    #     f.close()
    # for el in params:
    #     if el.split() and el.split()[0]=='DIMENSION':
    #         dim = el.split()[1]
    # history.setNbVar(dim)

    return history

def readLog_MW(path):
    # Reader de log de NOMAD et creer un objet history consequent

    # Regarde par le nom les specs de la run
    file=path.split('\\')[-1]
    name = file.split('_')
    ext = name[-1].split('.')[2]
    name[-1]=name[-1].split('.')[0]
    name.append(ext)

    #Erreur si on a pas un file history
    if name[2]!='history':
        print('file provided is not of the right format')
        return

    #On cree un objet history
    history=History.History()

    #Nom, Classe, solveur et parametre de resolution du probleme
    history.setProblem(str(name[0])+str(name[1]))
    history.setProblemNumber(str(name[0]))
    history.setProblemClass(str(name[1]))
    history.setSeed(str(name[3]))
    history.setAlgo(str(name[4][0]))
    history.setStrat(str(name[4][1:]))
    history.setSolver('NOMAD')

    # Ouvrir le history.txt
    with open(path, 'r') as file:
        iniFile = file.readlines()
        file.close()

    # Mettre la history dans l'objet
    nbIteration = len(iniFile) #nombre de lignes dans le fichier
    table = []  # initialisation de ma liste
    for x in range(0, nbIteration):
        # Pour chaque ligne de mon history je dois
        # creer une liste
        # appender la liste a l indice x du array
        ligne = list(map(float, (iniFile[x]).split()))  # creer la ligne de float
        table.append(ligne)  # ajoute a la table
    history.setTable(table)

    # Determiner la dimension du probleme
    paramPath = path[:-(len(path.split('\\')[-1]))]
    paramName = history.getSeed()+'_param.txt'
    paramFile = paramPath+paramName

    with open(paramFile, 'r') as f:
        # Ouvrir le parameters.txt
        params = f.readlines()
        f.close()
    for el in params:
        if el.split() and el.split()[0]=='DIMENSION':
            dim = el.split()[1]
    history.setNbVar(dim)

    return history


#Génère des fichiers paramètres avec plusieurs points de départs différents
# À partir d'un fichier paramètre
def generateParametersFiles(file,pts):
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

    ## Créer un nouveau fichier paramètre dans lequel
    ## on introduit le nouveau point de départ
    fileNameSplit = file[0:-4].split('_')
    problemName = fileNameSplit[0]
    typeOfFile = fileNameSplit[1]
    parametersOfResolution = fileNameSplit[2]
    ext = file[-4:]

    ## Definie des variables pour la génération
    numberPoints=npy.shape(pts)[0]
    dim = npy.shape(pts)[1]

    ## On modifie la table à imprimer avec les nouveaux noms de fichiers en parametres et les nouveaux points de depart
    for x in range(0,numberPoints):
        typeOfFile = 'parameters'
        newFileName = problemName + '_' + typeOfFile + '_' + parametersOfResolution + '_'+ str((x + 1)) + ext
        for ligne in table:
            if ligne and ligne[0] == 'X0':
                for y in range(0,dim):
                    ligne[2+y]=pts[x,y]
            if ligne and ligne[0]=='HISTORY_FILE':
                typeOfFile = 'history'
                ligne[1]= problemName + '_' + typeOfFile + '_' + parametersOfResolution + '_'+ str((x + 1)) + ext
            if ligne and ligne[0]=='SOLUTION_FILE':
                typeOfFile = 'solution'
                ligne[1]=problemName + '_' + typeOfFile + '_' + parametersOfResolution + '_'+ str((x + 1)) + ext
            if ligne and ligne[0]=='STATS_FILE':
                typeOfFile = 'stats'
                ligne[1] = problemName + '_' + typeOfFile + '_' + parametersOfResolution + '_' + str((x + 1)) + ext
        ## Ici on inscrit table dans un fichier
        thefile = open(newFileName, 'w')
        for item in table:
            for subItem in item:
                thefile.write('%s '% subItem)
            thefile.write('\n')
        thefile.close()

    #Genere n fichiers basés sur le file donné en entré

    return

