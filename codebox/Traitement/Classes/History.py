import numpy as npy
import copy


# La classe history sert de format pour une histoire des evaluations pour nimporte quel solveur


class History:
    #   Initialisations
    def __init__(self):
        # self.paramlist=file.split('_')
        # self.paramlist[-1]=self.paramlist[-1].split('.')[0]
        self.solver = 'undefined'
        self.strat = 'undefined'
        self.problem = 'undefined'
        self.problemNumber = 'undefined'  # si pas avec moré wild...
        self.problemClass = 'undefined'
        self.seed = 'undefined'
        self.algo = 'undefined'
        self.startpoint = 'undefined'
        self.nbVar = 1
        self.instance = ''
        self.opportunism = 'undefined'
        self.table = npy.array([])
        self.bbOutputType = []
        self.cleaned = False

    #   Print
    def __str__(self):
        return self.problem + "_" + self.solver + "_" + self.algo + self.strat + self.instance + "_" + self.getSeed()

    #   Getters and setters
    def getSolver(self):
        return self.solver

    def setSolver(self, entry):
        self.solver = entry
        return

    def getStrat(self):
        return self.strat

    def setStrat(self, entry):
        self.strat = entry
        return

    def getProblem(self):
        return self.solver

    def setProblem(self, entry):
        self.problem = entry
        return

    def setProblemNumber(self, entry):
        self.problemNumber = entry
        return

    def getProblemNumber(self):
        return self.problemNumber

    def setProblemClass(self, entry):
        self.problemClass = entry
        return

    def getProblemClass(self):
        return self.problemClass

    def setSeed(self, entry):
        self.seed = entry
        return

    def getSeed(self):
        return self.seed

    def getNbVar(self):
        return self.nbVar

    def setNbVar(self, entry):
        self.nbVar = entry
        return

    def getAlgo(self):
        return self.algo

    def setAlgo(self, entry):
        self.algo = entry
        return

    def getInstance(self):
        return self.instance

    def setInstance(self, entry):
        self.instance = entry
        return

    def getStartpoint(self):
        return self.startpoint

    def setStartpoint(self, entry):
        self.startpoint = entry
        return

    def getTable(self):
        return self.table

    def setTable(self, array):
        self.table = array
        return

    def getBbOutputType(self):
        return self.bbOutputType

    def setBbOutputType(self, arg):
        self.bbOutputType = arg
        return

    # Nettoyer la table en retenant que
    def clean(self):
        currentbest = 10 ** 100
        newList = []
        tempArray = npy.array(self.table)

        # Trouver le nombre de ligne dans la matrice
        nbLine = tempArray.shape[0]
        # nbColumn = tempArray.shape[1]
        # nbVar = int(self.getNbVar())

        # Si la table est vide on fait rien
        if self.table == ([]):
            return

        if self.cleaned:
            return

        # Si la table a un objet on la clean

        for x in range(0, nbLine):
            if tempArray[x, -1] < currentbest:
                # Beaucoup commentaires pour trucs qui marchent pas
                # violated = False

                # Si on a des contraintes, c'est a dire que il y a plus que les variables et la solution
                # Commente toute car ce n'est pas comme ça que ça marche

                # if nbVar != nbColumn:
                #
                #     #Si une contrainte est violée
                #     for i in range(nbVar+1,nbColumn):
                #         if self.table[x,i]>0:
                #             violated = True

                # Si c'est fructueux et que il n'y a pas de violation de contraintes
                # if not violated:
                #     currentbest = tempArray[x,-1]
                #     newList.append([int((x+1)),currentbest])

                currentbest = tempArray[x, -1]
                newList.append([int((x + 1)), currentbest])

        # newlist = npy.array(newlist)
        self.table = newList
        self.cleaned = True
        return

    def cleanConstrained(self):
        currentbest = 10 ** 100
        newList = []
        tempArray = npy.array(self.table)

        # Trouver le nombre de ligne dans la matrice
        nbLine = tempArray.shape[0]
        # nbColumn = tempArray.shape[1]
        # nbVar = int(self.getNbVar())

        # Si la table est vide on fait rien
        if self.table == ([]):
            return

        if self.cleaned:
            return

        # Trouver l'indice dans une ligne pour l'objectif
        obj_ind = int(self.nbVar) + int(self.bbOutputType.index('OBJ'))

        # Trouver les indices dans une ligne pour lesquels on a un PB
        pb_ind = [int(self.nbVar) + int(i) for i, x in enumerate(self.bbOutputType) if x == "PB"]

        # Trouver les indices dans une ligne pour lesquels on a un EB
        eb_ind = [int(self.nbVar) + int(i) for i, x in enumerate(self.bbOutputType) if x == "EB"]

        # Si la table a un objet on la clean
        for x in range(0, nbLine):

            # Savoir si le point est realisable
            realisable = True
            for i in pb_ind:
                if tempArray[x, i] > 0:
                    realisable = False
            for i in eb_ind:
                if tempArray[x, i] > 0:
                    realisable = False

            if tempArray[x, obj_ind] < currentbest and realisable:
                # Beaucoup commentaires pour trucs qui marchent pas
                # violated = False

                # Si on a des contraintes, c'est a dire que il y a plus que les variables et la solution
                # Commente toute car ce n'est pas comme ça que ça marche

                # if nbVar != nbColumn:
                #
                #     #Si une contrainte est violée
                #     for i in range(nbVar+1,nbColumn):
                #         if self.table[x,i]>0:
                #             violated = True

                # Si c'est fructueux et que il n'y a pas de violation de contraintes
                # if not violated:
                #     currentbest = tempArray[x,-1]
                #     newList.append([int((x+1)),currentbest])

                currentbest = tempArray[x, obj_ind]
                newList.append([int((x + 1)), currentbest])

        # newlist = npy.array(newlist)
        self.table = newList
        self.cleaned = True
        return

    def findBestSolution(self):
        temporaryHistory = copy.deepcopy(self)
        temporaryTable = npy.array(temporaryHistory.table)
        nbLine = temporaryTable.shape[0]
        if not temporaryTable.shape[0]==0:
            nbColumn = temporaryTable.shape[1]
            best = temporaryTable[(nbLine - 1), (nbColumn - 1)]
        else:
            best = 10**1000
        return best
