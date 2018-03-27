import numpy as npy
import Classes.History as History
import matplotlib.pyplot as plt


#La classe history sert de format pour une histoire des evaluations pour nimporte quel solveur


class HistorySet:

#   Initialisations
    def __init__(self):
        self.historyList = []
        self.numberProblem = '1'
        self.numberStrat = '1'
        self.numberSeed = '1'
        self.prolemClass = 'undefined'
        self.algo = 'undefined'
        self.opportunism = 'og'
        self.startpoint = 'undefined'

#   Getters and setters
    def getNumberProblem(self):
        return self.numberProblem

    def setNumberProblem(self, entry):
        self.numberProblem = entry
        return

    def getstartpoint(self):
        return self.startpoint

    def setstartpoint(self, entry):
        self.startpoint = entry
        return

    def getNumberStrat(self):
        return self.numberStrat

    def setNumberStrat(self, entry):
        self.numberStrat = entry
        return

    def getNumberSeed(self):
        return self.numberSeed

    def setNumberSeed(self, entry):
        self.numberSeed = entry
        return

    def getAlgo(self):
        return self.algo

    def setAlgo(self, entry):
        self.algo = entry
        return

    def getProblemClass(self):
        return self.problemClass

    def setProblemClass(self, entry):
        self.problemClass = entry
        return

    def getOpportunism(self):
        return self.opportunism

    def setOpportunism(self, entry):
        self.opportunism = entry
        return

    def getHistoryList(self):
        return self.historyList

    def addHistory(self,entry):
        if type(entry) is History.History:
            self.historyList.append(entry)
        else:
            print('Objet non ajouté a l ensemble d histoires car pas de la classe History')
        return

#   Trace de profils

    def plotPerformance(self,ratio, log):

        #Dictionnaire pour les meilleures solution de chaque probleme
        bestDict = {}

        #On trouve les meilleures solutions de chaque problème
        # Marche meme si on a différentes seeds
        for history in self.historyList:
            currentBest=history.findBestSolution
            if (history.problem) not in bestDict: #Clé du dictionnaire : %probname
                bestDict[history.problem]=currentBest
            elif (bestDict[history.problem]>currentBest):
                bestDict[history.problem]=currentBest

        #Doit retourner le nombre d'iterations que ca prends pour satisfaire le test
        #Pour chaque resolution
        # equivalent à t(p,s)
        nbItDict = {} #pour le nombre de iteration
        bestNbItDict = {} # meilleur par probleme
        whoHasBest = {}
        for history in self.historyList:
            tempArray = npy.array(history.getTable())
            nbLigne = len(history.table)
            #Itere sur les lignes
            for x in range(0, nbLigne):
                #Si le test est satisfait on append au dic avec key history : le nb d'iteration
                if (tempArray[0,1]-tempArray[x,1])>=(1-ratio)*(tempArray[0,1]-bestDict[history.problem]):
                    nbItDict[history]=tempArray[x,0]
                    break
            #Si le test n'est jamais satisfait
            if history not in nbItDict:
                nbItDict[history] = 1000000

        # Créer un dictionnaire avec key = strategie, objet = liste des profils
        for history in self.historyList:
            if (history.problem) not in bestNbItDict:
                bestNbItDict[history.problem]=nbItDict[history]
                whoHasBest[history.problem]=history.getStrat()
            elif nbItDict[history]<bestNbItDict[history.problem]:
                bestNbItDict[history.problem]=nbItDict[history]
                whoHasBest[history.problem] = history.getStrat()

        # r(p,s)
        perfRatioDict={}
        for x in self.historyList:
            if x.strat not in perfRatioDict:
                perfRatioDict[x.strat]=[]
                perfRatioDict[x.strat].append(nbItDict[x] / bestNbItDict[x.problem])
            else:
                perfRatioDict[x.strat].append(nbItDict[x] / bestNbItDict[x.problem])

        # Ordonner les ratio dans le dictionnaire et créer les profils
        sortedPerfRatioDict = {}
        x,y,x2,y2 = {},{},{},{}
        for strat in perfRatioDict:
            sortedPerfRatioDict[strat]=sorted(perfRatioDict[strat])
            x[strat],y[strat]=[],[]
            nbProbTraite = 0
            # Cette boucle créer les profils de performance à tracer
            for pt in sortedPerfRatioDict[strat]:
                x[strat].append(pt)
                x[strat].append(pt)
                y[strat].append(nbProbTraite / len(perfRatioDict[strat]))
                nbProbTraite=nbProbTraite +1
                y[strat].append(nbProbTraite/len(perfRatioDict[strat]))
            x2[strat] = HistorySet.markerize(x[strat],13)
            y2[strat] = HistorySet.markerize(y[strat], 13)

        #Définition de la nomenclature pour les plots
        nomenclature = {'n': 'Sans opport.', 'ol': 'Lexico', 'os': 'Succes', 'om': 'Modeles', 'g': 'GPS',
                        'm': 'MADS', 'gss': 'GSS', 'or': 'Aleatoire', 'c': 'CS', 'oo': 'Omniscient',
                        '0n': 'Negative-Omni.','i' : 'imfil', 'on' : 'Negative-Omni',
                        0.1: '1E-1', 0.01: '1E-2', 0.001: '1E-3', 0.0001: '1E-4', 0.00001: '1E-5', 0.000001: '1E-6',
                        0.0000001: '1E-7'}
        colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
        markers = ('o','v','^','s','+','x','*')
        linestyles = ['-', '--', '-.', ':','-','--','-.',':']
        color_index = 0
        marker_index = 0
        linestyle_index = 0

        # Plot
        if log == True:
            for strat in sortedPerfRatioDict:
                plt.step(npy.log10(x[strat]), y[strat],linestyle=linestyles[linestyle_index], color=colors[color_index])
                plt.plot(npy.log10(x2[strat]), y2[strat], marker=markers[marker_index],linestyle='None', color=colors[color_index], label = nomenclature[strat])
                color_index = color_index + 1
                marker_index = marker_index +1
                linestyle_index = linestyle_index + 1

        else :
            for strat in sortedPerfRatioDict:
                plt.step(x[strat], y[strat],linestyle=linestyles[linestyle_index], color=colors[color_index])
                plt.plot(x2[strat], y2[strat], marker=markers[marker_index],linestyle='None', color=colors[color_index], label = nomenclature[strat])
                color_index = color_index + 1
                marker_index = marker_index +1
                linestyle_index = linestyle_index + 1

        #Mettre graphe beau
        plt.ylim((0, 1.01))
        if log == True:
            plt.xlim((0, 1.1))
            plt.xlabel('Ratio de performance (log)')
        else :
            plt.xlim((1,10))
            plt.xlabel('Ratio de performance')
        plt.ylabel('Proportion de problème résolus')
        titre = 'Profil de performance,' + r'$\tau$' + '=' + str(
            ratio)
        plt.title(titre)
        nameoffig = 'perf_' + self.algo + '_' + self.problemClass + '_' + nomenclature[ratio] + self.opportunism
        if log == True:
            nameoffig = nameoffig + '_log'
        plt.savefig('plot\\'+nameoffig + '.png')
        plt.clf()
        plt.close()
        return

    def plotData(self, ratio, log):

        # Dictionnaire pour les meilleures solution de chaque probleme
        bestDict = {}
        iniDict = {}

        # On trouve les meilleures solutions de chaque problème
        # Marche meme si on a différentes seeds
        for history in self.historyList:

            ## Portion pour bestDict
            currentBest = history.findBestSolution()
            if (history.problem) not in bestDict:  # Clé du dictionnaire : %probname
                bestDict[history.problem] = currentBest
            elif (bestDict[history.problem] > currentBest):
                bestDict[history.problem] = currentBest

            ## Portion pour iniDict
            if (history.problem) not in iniDict:  # Clé du dictionnaire : %probname
                iniDict[history.problem] = []
            if history.table: # Si la liste n'est pas vide
                iniDict[history.problem].append(npy.array(history.getTable())[0, 1])
            else:
                iniDict[history.problem].append(10**100)

        ini_avgDict = {}
        if self.problemClass == 'CONSTRAINED'or self.problemClass == 'STYRENE':
            for key in iniDict:
                somme = sum(iniDict[key][i] for i in range(len(iniDict[key])) if iniDict[key][i] < 10**99)
                taille = len([i for i in range(len(iniDict[key])) if iniDict[key][i] < 10**99])
                if taille == 0:
                    taille =1
                ini_avgDict[key] = somme/taille

        # Doit retourner le nombre d'iterations que ca prends pour satisfaire le test
        # Pour chaque resolution
        # equivalent à t(p,s)
        nbItDict = {}  # pour le nombre de iteration
        for history in self.historyList:
            tempArray = npy.array(history.getTable())
            nbLigne = len(history.table)

            # Trouver le point initial, soit moyenne des pts realisables ou juste la premiere ligne de cleaned
            if self.problemClass == 'CONSTRAINED' or self.problemClass == 'STYRENE':
                ini_point_value = ini_avgDict[history.problem]
            else:
                ini_point_value = tempArray[0, 1]

            # Itere sur les lignes
            for x in range(0, nbLigne):
                # Si le test est satisfait on append au dic avec key history : le nb d'iteration
                if (ini_point_value- tempArray[x, 1]) >= (1 - ratio) * (ini_point_value - bestDict[history.problem]):
                    nbItDict[history] = tempArray[x, 0]
                    break
            # Si le test n'est jamais satisfait
            if history not in nbItDict:
                nbItDict[history] = 10**100

        dataDict = {}
        for x in self.historyList:
            key = (x.algo,x.strat) # un tuple avec les algo et strat
            if key not in dataDict:
                dataDict[key]=[]
                dataDict[key].append(nbItDict[x] / (int(x.nbVar)+1))
            else:
                dataDict[key].append(nbItDict[x] / (int(x.nbVar)+1))

        # Ordonner les ratio dans le dictionnaire et créer les profils
        sortedDataDict = {}
        x, y, x2, y2 = {}, {}, {}, {}
        for key in dataDict:
            sortedDataDict[key] = sorted(dataDict[key])
            x[key], y[key] = [], []
            nbProbTraite = 0
            # Cette boucle créer les profils de performance à tracer
            for pt in sortedDataDict[key]:
                x[key].append(max(pt,1.1))
                x[key].append(max(pt,1.1))
                y[key].append(nbProbTraite / len(dataDict[key]))
                nbProbTraite = nbProbTraite + 1
                y[key].append(nbProbTraite / len(dataDict[key]))
            x2[key] = HistorySet.markerize(x[key], 13)
            y2[key] = HistorySet.markerize(y[key], 13)

        # Définition de la nomenclature pour les plots
        nomenclature = {'n': 'Sans opport.', 'ol': 'Déterministe', 'os': 'Succes', 'om': 'Modeles', 'g': 'GPS',
                        'm': 'MADS', 'gss': 'GSS', 'or': 'Aleatoire', 'c': 'CS', 'oo': 'Omniscient',
                        '0n': 'Inverse-Omni','i' : 'imfil', 'on' : 'Inverse-Omni', 't' : 'Defaut',
                        0.1: '1E-1', 0.01: '1E-2', 0.001: '1E-3', 0.0001: '1E-4', 0.00001: '1E-5', 0.000001: '1E-6',
                        0.0000001: '1E-7'}
        colors = ('g', 'b', 'r', 'c', 'm', 'y', 'k')
        colors_by_strat = {'c': 'g', 'g': 'b', 'm': 'r', 't': 'c', 'n': 'g', 'ol': 'b', 'os': 'r', 'om': 'c', 'or': 'm',
                           'oo': 'y', '0n': 'k','on':'k'}
        markers = ('o','v','^','s','+','x','*')
        markers_by_strat = {'c': 'o', 'g': 'v', 'm': '^', 't': 's','n': 'o', 'ol': 'v', 'os': '^', 'om': 's', 'or': '+',
                           'oo': 'x', '0n': '*','on':'*'}
        linestyles = ['-', '--', '-.', ':','-','--','-.',':']
        linestyles_by_strat = {'c': '-', 'g': '--', 'm': '-.', 't': ':', 'n': '-', 'ol': '--', 'os': '-.', 'om': ':', 'or': '-',
                           'oo': '--', '0n': '-.','on':'-.'}

        # Plot
        fig = plt.figure()
        if log == True:
            for key in sortedDataDict:
                plt.step(npy.log10(x[key]), y[key],linestyle=linestyles_by_strat[key[1]], color=colors_by_strat[key[1]])
                plt.plot(npy.log10(x2[key]), y2[key], marker=markers_by_strat[key[1]],linestyle='None', color=colors_by_strat[key[1]], label = nomenclature[key[1]])
        else :
            for key in sortedDataDict:
                plt.step(x[key], y[key], linestyle=linestyles_by_strat[key[1]],
                         color=colors_by_strat[key[1]])
                plt.plot(x2[key], y2[key], marker=markers_by_strat[key[1]], linestyle='None',
                         color=colors_by_strat[key[1]], label=nomenclature[key[1]])
        # plt.legend()
        # Mettre graphe beau
        plt.ylim((0, 1.01))
        if log:
            plt.xlim((0, 3))
            plt.xlabel('Nombre de gradient simplex (log)')
        else:
            plt.xlim((1,1000))
            plt.xlabel('Nombre de gradient simplex')
        plt.ylabel('Proportion de problème résolus')
        titre = 'Profil de donnees,' + r'$\tau$' + '=' + nomenclature[ratio]
        plt.title(titre)
        nameoffig = 'data_' + self.algo + '_' + self.problemClass + '_' + nomenclature[ratio] + self.opportunism
        if log:
            nameoffig = nameoffig + '_log'
        plt.savefig('plot\\' + nameoffig + '.png')
        plt.close(fig)
        # ################################
        # # Uncomment pour tracer la légende
        # # Dummy figure pour plotter mes affaires
        # fig_legend2 = plt.figure()
        # for key in sortedDataDict:
        #     plt.plot(npy.log10(x2[key]), y2[key],  marker=markers_by_strat[key[1]], linestyle=linestyles_by_strat[key[1]],
        #              color=colors_by_strat[key[1]], label=nomenclature[key[1]])
        #
        # fig_legend = plt.figure(figsize=(10, 1))
        # ax = fig.add_subplot(111)
        # handles, labels = fig_legend2.axes[0].get_legend_handles_labels()
        # fig_legend.legend(handles, labels, loc='center',frameon = False, ncol = 7)
        # plt.show()
        # fig_legend.savefig('legend_more_wild2')
        #################################

        plt.close()


        # for strat in sortedDataDict:
        #     ax.step(x[strat], y[strat],linestyle=linestyles[linestyle_index], color=colors[color_index])
        #     ax.plot(x2[strat], y2[strat], marker=markers[marker_index],linestyle='None', color=colors[color_index], label = nomenclature[strat])
        #     color_index = color_index + 1
        #     marker_index = marker_index +1
        #     linestyle_index = linestyle_index + 1




        plt.clf()

        # plot legend out of plot        # CE CODE EST POUR REFAIRE LA LEGENDE AU BESOIN
        # Trace legende en dehors
        # fig = plt.figure()
        # figlegend = plt.figure(figsize=(2, 2))
        # ax = fig.add_subplot(111)
        # lines = ax.plot(range(10), npy.random.random(10), range(10), npy.random.random(10),range(10), npy.random.random(10),range(10), npy.random.random(10),range(10), npy.random.random(10),range(10), npy.random.random(10),range(10), npy.random.random(10))

        return

    def plot_convergence_all_curves(self):

        # COURBES

        # On prends la liste d'history
        histories = self.getHistoryList()

        # Le graphe
        nomenclature = {'n': 'Sans opport.', 'ol': 'Lexicographique', 'os': 'Succes', 'om': 'Modeles', 'g': 'GPS',
                        'm': 'MADS', 'gss': 'GSS', 'or': 'Aleatoire', 'c': 'CS', 'oo': 'Omniscient',
                        '0n': 'Inverse-Omni','i' : 'imfil', 'on' : 'Inverse-Omni', 't' : 'Defaut',
                        0.1: '1E-1', 0.01: '1E-2', 0.001: '1E-3', 0.0001: '1E-4', 0.00001: '1E-5', 0.000001: '1E-6',
                        0.0000001: '1E-7'}
        colors_by_strat = {'c': 'g', 'g': 'b', 'm': 'r', 't': 'c', 'n': 'g', 'ol': 'b', 'os': 'r', 'om': 'c', 'or': 'm',
                           'oo': 'y', '0n': 'k','on':'k'}
        markers_by_strat = {'c': 'o', 'g': 'v', 'm': '^', 't': 's','n': 'o', 'ol': 'v', 'os': '^', 'om': 's', 'or': '+',
                           'oo': 'x', '0n': '*','on':'*'}
        linestyles_by_strat = {'c': '-', 'g': '--', 'm': '-.', 't': ':', 'n': '-', 'ol': '--', 'os': '-', 'om': '-', 'or': '-',
                           'oo': '-', '0n': '-','on':'-'}
        fig = plt.figure()
        xlim = 800
        for run in histories:
            if not run.table:
                run_table = npy.array([[0,0],[0,1]]) # Dummy table pour si la premiere eval etait un echec
            else:
                run_table = npy.array(run.table)
                run_table = npy.vstack((run_table, [xlim, run_table[-1,1]]))
            # markers[curve_styles[run.getStrat()]] # POUR LES MARQUEURS AU BESOIN

            # Mettre une ligne verticale pour le debut
            if run_table[0,0] != 1:
                run_table = npy.vstack(([run_table[0, 0], 1], run_table))

            plt.step(run_table[:, 0], run_table[:, 1], linestyle=linestyles_by_strat[run.getStrat()],
                     color=colors_by_strat[run.getStrat()],
                 label=nomenclature[run.getStrat()],lw=0.5)
            plt.xlim((0, xlim))


        # Mettre ca beau
        plt.xlabel('Nombre d\'évaluations')
        plt.ylabel('Valeur de la fonction-objectif')

        # La legende
        handles, labels = plt.gca().get_legend_handles_labels()
        newLabels, newHandles = [], []
        for handle, label in zip(handles, labels):
            if label not in newLabels:
                newLabels.append(label)
                newHandles.append(handle)
        plt.legend(newHandles, newLabels,loc='upper right')
        titre = 'Convergence avec ' + (newLabels[-1])
        plt.title(titre)
        nameoffig = 'conv_' + self.algo+self.opportunism + '_' + self.problemClass+self.startpoint + '_' + '_'.join(newLabels)
        plt.savefig('plot\\'+nameoffig + '.png')

    def markerize(entry,number):
        # Retourne une liste avec 8 points à peu pres equidistant
        if len(entry)<=number:
            result = entry
        else:
            gap = int(npy.floor(len(entry)/number))
            indexes = []
            index=0
            result = []
            for i in range(number):
                index = index+gap
                indexes.append(index)
                result.append(entry[index])
        return result


    def plotDataopp(self, ratio, log):

        # Dictionnaire pour les meilleures solution de chaque probleme
        bestDict = {}
        iniDict = {}

        # On trouve les meilleures solutions de chaque problème
        # Marche meme si on a différentes seeds
        for history in self.historyList:

            ## Portion pour bestDict
            currentBest = history.findBestSolution()
            if (history.problem) not in bestDict:  # Clé du dictionnaire : %probname
                bestDict[history.problem] = currentBest
            elif (bestDict[history.problem] > currentBest):
                bestDict[history.problem] = currentBest

            ## Portion pour iniDict
            if (history.problem) not in iniDict:  # Clé du dictionnaire : %probname
                iniDict[history.problem] = []
            if history.table: # Si la liste n'est pas vide
                iniDict[history.problem].append(npy.array(history.getTable())[0, 1])
            else:
                iniDict[history.problem].append(10**100)

        ini_avgDict = {}
        if self.problemClass == 'CONSTRAINED'or self.problemClass == 'STYRENE':
            for key in iniDict:
                somme = sum(iniDict[key][i] for i in range(len(iniDict[key])) if iniDict[key][i] < 10**99)
                taille = len([i for i in range(len(iniDict[key])) if iniDict[key][i] < 10**99])
                if taille == 0:
                    taille =1
                ini_avgDict[key] = somme/taille

        # Doit retourner le nombre d'iterations que ca prends pour satisfaire le test
        # Pour chaque resolution
        # equivalent à t(p,s)
        nbItDict = {}  # pour le nombre de iteration
        for history in self.historyList:
            tempArray = npy.array(history.getTable())
            nbLigne = len(history.table)

            # Trouver le point initial, soit moyenne des pts realisables ou juste la premiere ligne de cleaned
            if self.problemClass == 'CONSTRAINED' or self.problemClass == 'STYRENE':
                ini_point_value = ini_avgDict[history.problem]
            else:
                ini_point_value = tempArray[0, 1]

            # Itere sur les lignes
            for x in range(0, nbLigne):
                # Si le test est satisfait on append au dic avec key history : le nb d'iteration
                if (ini_point_value- tempArray[x, 1]) >= (1 - ratio) * (ini_point_value - bestDict[history.problem]):
                    nbItDict[history] = tempArray[x, 0]
                    break
            # Si le test n'est jamais satisfait
            if history not in nbItDict:
                nbItDict[history] = 10**100

        dataDict = {}
        for x in self.historyList:
            key = (x.algo,x.opportunism) # un tuple avec les algo et strat
            if key not in dataDict:
                dataDict[key]=[]
                dataDict[key].append(nbItDict[x] / (int(x.nbVar)+1))
            else:
                dataDict[key].append(nbItDict[x] / (int(x.nbVar)+1))

        # Ordonner les ratio dans le dictionnaire et créer les profils
        sortedDataDict = {}
        x, y, x2, y2 = {}, {}, {}, {}
        for key in dataDict:
            sortedDataDict[key] = sorted(dataDict[key])
            x[key], y[key] = [], []
            nbProbTraite = 0
            # Cette boucle créer les profils de performance à tracer
            for pt in sortedDataDict[key]:
                x[key].append(max(pt,1.1))
                x[key].append(max(pt,1.1))
                y[key].append(nbProbTraite / len(dataDict[key]))
                nbProbTraite = nbProbTraite + 1
                y[key].append(nbProbTraite / len(dataDict[key]))
            x2[key] = HistorySet.markerize(x[key], 13)
            y2[key] = HistorySet.markerize(y[key], 13)

        # Définition de la nomenclature pour les plots
        nomenclature = {'n': 'Sans opport.', 'ol': 'Déterministe', 'os': 'Succes', 'om': 'Modeles', 'g': 'GPS',
                        'm': 'MADS', 'gss': 'GSS', 'or': 'Aleatoire', 'c': 'CS', 'oo': 'Omniscient',
                        '0n': 'Inverse-Omni','i' : 'imfil', 'on' : 'Inverse-Omni', 't' : 'Defaut',
                        0.1: '1E-1', 0.01: '1E-2', 0.001: '1E-3', 0.0001: '1E-4', 0.00001: '1E-5', 0.000001: '1E-6',
                        0.0000001: '1E-7', 'OG' : 'Simple','SECSUC':'2e succes','MINEVAL':'Minimum n/2 evaluations'}
        colors = ('g', 'b', 'r', 'c', 'm', 'y', 'k')
        colors_by_strat = {'c': 'g', 'g': 'b', 'm': 'r', 't': 'c', 'n': 'k', 'ol': 'b', 'os': 'r', 'om': 'c', 'or': 'm',
                           'oo': 'y', '0n': 'k','on':'k','OG':'g','SECSUC':'b','MINEVAL':'r'}
        markers = ('o','v','^','s','+','x','*')
        markers_by_strat = {'c': 'o', 'g': 'v', 'm': '^', 't': 's','n': 'o', 'ol': 'v', 'os': '^', 'om': 's', 'or': '+',
                           'oo': 'x', '0n': '*','on':'*','OG':'o','SECSUC':'v','MINEVAL':'^'}
        linestyles = ['-', '--', '-.', ':','-','--','-.',':']
        linestyles_by_strat = {'c': '-', 'g': '--', 'm': '-.', 't': ':', 'n': '-', 'ol': '--', 'os': '-.', 'om': ':', 'or': '-',
                           'oo': '--', '0n': '-.','on':'-.','OG':'-','SECSUC':'-','MINEVAL':'-'}

        # Plot
        fig = plt.figure()
        if log == True:
            for key in sortedDataDict:
                plt.step(npy.log10(x[key]), y[key],linestyle=linestyles_by_strat[key[1]], color=colors_by_strat[key[1]])
                plt.plot(npy.log10(x2[key]), y2[key], marker=markers_by_strat[key[1]],linestyle='None', color=colors_by_strat[key[1]], label = nomenclature[key[1]])
        else :
            for key in sortedDataDict:
                plt.step(x[key], y[key], linestyle=linestyles_by_strat[key[1]],
                         color=colors_by_strat[key[1]])
                plt.plot(x2[key], y2[key], marker=markers_by_strat[key[1]], linestyle='None',
                         color=colors_by_strat[key[1]], label=nomenclature[key[1]])
        # plt.legend()
        # Mettre graphe beau
        plt.ylim((0, 1.01))
        if log:
            plt.xlim((0, 3))
            plt.xlabel('Nombre de gradient simplex (log)')
        else:
            plt.xlim((1,1000))
            plt.xlabel('Nombre de gradient simplex')
        plt.ylabel('Proportion de problème résolus')
        titre = 'Profil de donnees,' + r'$\tau$' + '=' + nomenclature[ratio]
        plt.title(titre)
        nameoffig = 'data_' + self.algo + '_' + self.problemClass + '_' + nomenclature[ratio] + 'oppcomp'
        if log:
            nameoffig = nameoffig + '_log'
        plt.savefig('plot\\' + nameoffig + '.png')
        plt.close(fig)
        # ################################
        # # Uncomment pour tracer la légende
        # # Dummy figure pour plotter mes affaires
        # fig_legend2 = plt.figure()
        # for key in sortedDataDict:
        #     plt.plot(npy.log10(x2[key]), y2[key],  marker=markers_by_strat[key[1]], linestyle=linestyles_by_strat[key[1]],
        #              color=colors_by_strat[key[1]], label=nomenclature[key[1]])
        #
        # fig_legend = plt.figure(figsize=(10, 1))
        # ax = fig.add_subplot(111)
        # handles, labels = fig_legend2.axes[0].get_legend_handles_labels()
        # fig_legend.legend(handles, labels, loc='center',frameon = False, ncol = 7)
        # plt.show()
        # fig_legend.savefig('legend_more_wild2')
        #################################

        plt.close()


        # for strat in sortedDataDict:
        #     ax.step(x[strat], y[strat],linestyle=linestyles[linestyle_index], color=colors[color_index])
        #     ax.plot(x2[strat], y2[strat], marker=markers[marker_index],linestyle='None', color=colors[color_index], label = nomenclature[strat])
        #     color_index = color_index + 1
        #     marker_index = marker_index +1
        #     linestyle_index = linestyle_index + 1




        plt.clf()

        # plot legend out of plot        # CE CODE EST POUR REFAIRE LA LEGENDE AU BESOIN
        # Trace legende en dehors
        # fig = plt.figure()
        # figlegend = plt.figure(figsize=(2, 2))
        # ax = fig.add_subplot(111)
        # lines = ax.plot(range(10), npy.random.random(10), range(10), npy.random.random(10),range(10), npy.random.random(10),range(10), npy.random.random(10),range(10), npy.random.random(10),range(10), npy.random.random(10),range(10), npy.random.random(10))

        return