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

#   Getters and setters
    def getNumberProblem(self):
        return self.numberProblem

    def setNumberProblem(self, entry):
        self.numberProblem = entry
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
            currentBest=history.findBestSolution()
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
                        0.1: '01', 0.01: '001', 0.001: '0001'}
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
        nameoffig = 'perf_' + self.algo + '_' + self.problemClass + '_' + nomenclature[ratio]
        if log == True:
            nameoffig = nameoffig + '_log'
        plt.savefig(nameoffig + '.png')
        plt.clf()
        return

    def plotData(self, ratio, log):

        # Dictionnaire pour les meilleures solution de chaque probleme
        bestDict = {}

        # On trouve les meilleures solutions de chaque problème
        # Marche meme si on a différentes seeds
        for history in self.historyList:
            currentBest = history.findBestSolution()
            if (history.problem) not in bestDict:  # Clé du dictionnaire : %probname
                bestDict[history.problem] = currentBest
            elif (bestDict[history.problem] > currentBest):
                bestDict[history.problem] = currentBest

        # Doit retourner le nombre d'iterations que ca prends pour satisfaire le test
        # Pour chaque resolution
        # equivalent à t(p,s)
        nbItDict = {}  # pour le nombre de iteration
        for history in self.historyList:
            tempArray = npy.array(history.getTable())
            nbLigne = len(history.table)
            # Itere sur les lignes
            for x in range(0, nbLigne):
                # Si le test est satisfait on append au dic avec key history : le nb d'iteration
                if (tempArray[0, 1] - tempArray[x, 1]) >= (1 - ratio) * (tempArray[0, 1] - bestDict[history.problem]):
                    nbItDict[history] = tempArray[x, 0]
                    break
            # Si le test n'est jamais satisfait
            if history not in nbItDict:
                nbItDict[history] = 1000000

        dataDict = {}
        for x in self.historyList:
            if x.strat not in dataDict:
                dataDict[x.strat]=[]
                dataDict[x.strat].append(nbItDict[x] / (int(x.nbVar)+1))
            else:
                dataDict[x.strat].append(nbItDict[x] / (int(x.nbVar)+1))

        # Ordonner les ratio dans le dictionnaire et créer les profils
        sortedDataDict = {}
        x, y, x2, y2 = {}, {}, {}, {}
        for strat in dataDict:
            sortedDataDict[strat] = sorted(dataDict[strat])
            x[strat], y[strat] = [], []
            nbProbTraite = 0
            # Cette boucle créer les profils de performance à tracer
            for pt in sortedDataDict[strat]:
                x[strat].append(pt)
                x[strat].append(pt)
                y[strat].append(nbProbTraite / len(dataDict[strat]))
                nbProbTraite = nbProbTraite + 1
                y[strat].append(nbProbTraite / len(dataDict[strat]))
            x2[strat] = HistorySet.markerize(x[strat], 13)
            y2[strat] = HistorySet.markerize(y[strat], 13)

        # Définition de la nomenclature pour les plots
        nomenclature = {'n': 'Sans opport.', 'ol': 'Lexico', 'os': 'Succes', 'om': 'Modeles', 'g': 'GPS',
                        'm': 'MADS', 'gss': 'GSS', 'or': 'Aleatoire', 'c': 'CS', 'oo': 'Omniscient',
                        '0n': 'Negative-Omni.','i' : 'imfil', 'on' : 'Negative-Omni',
                        0.1: '01', 0.01: '001', 0.001: '0001'}
        colors = ('g', 'b', 'r', 'c', 'm', 'y', 'k')
        markers = ('o','v','^','s','+','x','*')
        linestyles = ['-', '--', '-.', ':','-','--','-.',':']
        color_index = 0
        marker_index = 0
        linestyle_index = 0

        # Plot
        fig = plt.figure()
        if log == True:
            for strat in sortedDataDict:
                plt.step(npy.log10(x[strat]), y[strat],linestyle=linestyles[linestyle_index], color=colors[color_index])
                plt.plot(npy.log10(x2[strat]), y2[strat], marker=markers[marker_index],linestyle='None', color=colors[color_index], label = nomenclature[strat])
                color_index = color_index + 1
                marker_index = marker_index +1
                linestyle_index = linestyle_index + 1
        else :
            for strat in sortedDataDict:
                plt.step(x[strat], y[strat],linestyle=linestyles[linestyle_index], color=colors[color_index])
                plt.plot(x2[strat], y2[strat], marker=markers[marker_index],linestyle='None', color=colors[color_index], label = nomenclature[strat])
                color_index = color_index + 1
                marker_index = marker_index +1
                linestyle_index = linestyle_index + 1
        plt.legend()
        # Mettre graphe beau
        plt.ylim((0, 1.01))
        if log == True:
            plt.xlim((0, 2))
            plt.xlabel('Nombre de gradient simplex (log)')
        else :
            plt.xlim((1,800))
            plt.xlabel('Nombre de gradient simplex')
        plt.ylabel('Proportion de problème résolus')
        titre = 'Profil de donnees,' + r'$\tau$' + '=' + str(
            ratio)
        plt.title(titre)
        nameoffig = 'data_' + self.algo + '_' + self.problemClass + '_' + nomenclature[ratio]
        if log == True:
            nameoffig = nameoffig + '_log'
        plt.savefig(nameoffig + '.png')


        # for strat in sortedDataDict:
        #     ax.step(x[strat], y[strat],linestyle=linestyles[linestyle_index], color=colors[color_index])
        #     ax.plot(x2[strat], y2[strat], marker=markers[marker_index],linestyle='None', color=colors[color_index], label = nomenclature[strat])
        #     color_index = color_index + 1
        #     marker_index = marker_index +1
        #     linestyle_index = linestyle_index + 1

        # # CE CODE EST POUR REFAIRE LA LEGENDE AU BESOIN
        # # Trace legende en dehors
        # color_index = 0
        # marker_index = 0
        # linestyle_index = 0
        # fig_legend = plt.figure(figsize=(10, 1))
        # ax = fig.add_subplot(111)
        # handles, labels = fig.axes[0].get_legend_handles_labels()
        # fig_legend.legend(handles, labels, loc='center',frameon = False, ncol = 7)
        # plt.show()
        # fig_legend.savefig('legend_more_wild')
        #
        plt.clf()

        # plot legend out of plot
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
        nomenclature = {'n': 'Sans opport.', 'ol': 'Lexico', 'os': 'Succes', 'om': 'Modeles', 'g': 'GPS',
                        'm': 'MADS', 'gss': 'GSS', 'or': 'Aleatoire', 'c': 'CS', 'oo': 'Omniscient',
                        '0n': 'Negative-Omni.', 'i': 'imfil', 'on': 'Negative-Omni',
                        0.1: '01', 0.01: '001', 0.001: '0001'}

        colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
        markers = ('o', 'v', '^', 's', '+', 'x', '*')
        linestyles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
        fig = plt.figure()
        index = 0
        curve_styles = {}
        xlim = 200
        color_for_strat = {'n':'b','ol':'g','os':'r','om':'c','oo':'y','or':'m','0n':'k'}
        for run in histories:
            if run.getStrat() not in curve_styles:
                curve_styles[run.getStrat()] = index
                index = index + 1
            if not run.table:
                run_table = npy.array([[0,0],[0,1]]) # Dummy table pour si la premiere eval etait un echec
            else:
                run_table = npy.array(run.table)
                run_table = npy.vstack((run_table, [xlim, run_table[-1,1]]))
            # markers[curve_styles[run.getStrat()]] # POUR LES MARQUEURS AU BESOIN
            plt.step(run_table[:, 0], run_table[:, 1], linestyle=linestyles[curve_styles[run.getStrat()]], color=color_for_strat[run.getStrat()],
                 label=nomenclature[run.getStrat()],lw=0.5)
            plt.xlim((0, xlim))


        # Mettre ca beau
        plt.xlabel('Nombre d''évaluations')
        plt.ylabel('Valeur de la fonction-objectif')

        # La legende
        handles, labels = plt.gca().get_legend_handles_labels()
        newLabels, newHandles = [], []
        for handle, label in zip(handles, labels):
            if label not in newLabels:
                newLabels.append(label)
                newHandles.append(handle)
        plt.legend(newHandles, newLabels,loc='best')
        strat_names_title = [nomenclature[x] for x in curve_styles]
        titre = 'Convergence sur ' + self.problemClass + ' ' + ' vs '.join(strat_names_title)
        plt.title(titre)
        nameoffig = 'conv_' + self.algo + '_' + self.problemClass + '_' + '_'.join(curve_styles)
        plt.savefig(nameoffig + '.png')


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