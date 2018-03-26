import pickle
import subprocess
import os.path
import numpy as npy
import Classes.HistorySet as HistorySet
import Classes.nomadFonctions as NOMAD
import Classes.hopspackFonctions as HOPSPACK
import Classes.imfilFonctions as imfil
import Classes.tousFonctions as fct


def test1():
    # plt.plot([1,2,3,4])
    # plt.ylabel('some numbers')
    # plt.show()
    historySet = HistorySet.HistorySet()

    history = NOMAD.readLog('bb3_history.0.txt')
    history.clean()
    print(history.table)
    historySet.addHistory(history)

    history = NOMAD.readLog('bb2_history_mol.0.txt')
    history.setNbVar(5)
    print(history.table)
    print(history.findBestSolution)
    history.clean()
    print(history.table)
    print(history)
    return


def test2():
    for x in set.historyList:
        print(x)
        print(x.table)

    [a, b, c, d, e] = set.plotPerformance(0.1)

    for x in a:
        print(x, a[x])
    for x in b:
        print(x, b[x])
    for x in c:
        print(x, c[x])
    for x in d:
        print(x, d[x])
    for x in e:
        print(x, e[x])
    print(len(a))
    # HistorySet.addHistory(history)

    # Trouver le meilleur de tous les history
    currentbest = 10 ^ 100
    for x in range(0, len(HistorySet.historyList)):
        currentHistory = HistorySet.historyList[x]
        if currentHistory.findBestSolution < currentbest:
            currentbest = currentHistory.findBestSolution

    # Faire les profils de performance


    # Faire les profils de donnees


    print(currentbest)
    return


def serialNomadRuns():
    # Rouler les problèmes en serie
    algo = ['g', 'm']
    problem = ['bb1', 'bb2', 'bb3']
    ordering = ['n', 'ol', 'os', 'om']
    currentname = ''
    for p in range(0, 3):
        for a in range(0, 2):
            for o in range(0, 4):
                currentname = '\"%NOMAD_HOME%\\bin\\nomad.exe\" ' + problem[p] + '_parameters_' + algo[a] + ordering[
                    o] + '.txt'
                print(currentname)
                subprocess.call(currentname, shell=True)
    return


def codeRapport1():
    #########################################
    ################ CODE POUR RAPPORT 1 ####
    algo = ['g', 'm']
    problem = ['bb1', 'bb2', 'bb3']
    ordering = ['n', 'ol', 'os', 'om']
    currentname = ''

    taux = [0.1, 0.01, 0.001]
    for a in algo:
        for x in taux:
            set = HistorySet.HistorySet()
            set.algo = a
            for p in range(0, 3):
                for o in range(0, 4):
                    nomFichier = problem[p] + "_history_" + a + ordering[o] + ".0.txt"
                    history = NOMAD.readLog(nomFichier)
                    history.setProblem(problem[p])
                    history.setSolver(a)
                    history.setStrat(ordering[o])

                    ##Faire une fonction pour trouver le nombre de var. (avec stats)
                    if p == 0:
                        history.setNbVar(4)
                    elif p == 1:
                        history.setNbVar(5)
                    else:
                        history.setNbVar(2)

                    set.addHistory(history)
            set.setNumberProblem(p + 1)
            set.setNumberStrat(o + 1)
            set.plotPerformance(x)
            # set.plotData(x)
            # for b in dic:
            #     print(b)
            #     print(dic[b])
    #####################################################
    #####################################################
    return


def codeRapport2():
    problems = ['bb1', 'bb2', 'bb3']
    algos = ['g', 'm']
    strats = ['n', 'ol', 'os', 'om']
    nbPts = 100

    for problem in problems:
        ## Un fichier de paramètre random juste pour generer des points et on les sauvegarde dans un fichier texte
        generateTemplateFileName = problem + '_parameters_gos.txt'
        pts = fct.generateStartPoints(generateTemplateFileName, nbPts)
        npy.savetxt((problem + '_pts.txt'), pts)

        ## Créer un fichier avec toujours les memes points
        for algo in algos:
            for strat in strats:
                parameterTemplateName = problem + '_parameters_' + algo + strat + '.txt'
                NOMAD.generateParametersFiles(parameterTemplateName, pts)

    for algo in algos:
        set = HistorySet.HistorySet()
        for problem in problems:
            for strat in strats:
                for number in range(0, nbPts):
                    # Lignes pour rouler nomad en serie avec toutes les instances
                    # currentname = '\"%NOMAD_HOME%\\bin\\nomad.exe\" ' + problem + '_parameters_' + algo + strat + '_' + str(number+1) +'.txt'
                    # subprocess.call(currentname, shell=True)
                    if (str(number + 1))[-1] == '0':
                        nomFichier = problem + '_history_' + algo + strat + '_' + str(number + 1) + '.txt'
                    else:
                        nomFichier = problem + '_history_' + algo + strat + '_' + str(number + 1) + '.0.txt'
                    history = NOMAD.readLog(nomFichier)
                    set.addHistory(history)
        set.setNumberProblem(len(problems) * nbPts)
        set.setNumberStrat(len(strats))
        set.setAlgo(algo)
        set.plotData(0.001)

    # test=NOMAD.readLog('bb1_history_gn.0.txt')

    return


def codeRapport3():
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om']

    for instance in instances:
        for type in types:
            # exename = instance+'_'+type+"\\bb.exe"
            # cppname = instance + '_' + type + "\\bb.cpp"
            # call(["g++", "-o", exename, cppname])
            for algo in algos:
                for strategy in strategies:
                    foldername = 'resultats' + instance + '_' + type + '\\' + algo + strategy
                    for seed in seeds:
                        filename = foldername + '\\' + seed + '_param.txt'
                        print(filename)
    return


def test4():
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om']
    for algo in algos:
        for type in types:
            set = HistorySet.HistorySet()
            for instance in instances:
                for strategy in strategies:
                    # exename = instance+'_'+type+"\\bb.exe"
                    # cppname = instance + '_' + type + "\\bb.cpp"
                    # call(["g++", "-o", exename, cppname])
                    foldername = 'resultats' + '\\' + instance + '_' + type + '\\' + algo + strategy
                    for seed in seeds:
                        historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                        filename = foldername + '\\' + historyfile
                        currentHist = NOMAD.readLog(filename)
                        set.addHistory(currentHist)
            with open(algo + type + '.pkl', 'wb') as output:
                pickle.dump(set, output, pickle.HIGHEST_PROTOCOL)
            del set


def test5():
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'c': 'CS', 'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om', 'or', 'oo', 'on']

    # Pre traitement des history en enlevant les non succes (on aurait pu prendre stats)
    for algo in algos:
        for type in types:
            dumpStrat = algo + type
            fileName = "pkl_algo_type\\" + algo + type + ".pkl"
            with open(fileName, 'rb') as f:
                set = pickle.load(f)
                f.close()

            # Setter les bons parametres pour le set
            set.setNumberProblem(len(instances))
            set.setNumberSeed(len(seeds))
            set.setNumberStrat(len(strategies))
            set.setAlgo(algo)

            # Nettoyer et garder seulement les succès
            for history in set.historyList:
                history.clean()
            set.setProblemClass(type)

            # Re pickler mais seulements les histoires nettoyées
            pickle.dump(set, open(fileName[:-4] + "_clean.pkl", "wb"), pickle.HIGHEST_PROTOCOL)
            del set

    return


def test6():
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om']
    ratios = [0.1, 0.01, 0.001]
    for algo in algos:
        for type in types:
            fileName = "pkl_algo_type\\" + algo + type
            with open(fileName + '_clean.pkl', "rb") as f:
                testSet = pickle.load(f)
                f.close()
            for ratio in ratios:
                testSet.plotPerformance(ratio)
                testSet.plotData(ratio)
                #  testSet.plotPerformance(0.1)


def test7():
    algo = 'g'
    ratio = 0.1
    type = 'SMOOTH'
    fileName = "pkl_algo_type\\" + algo + type
    with open(fileName + '_clean.pkl', "rb") as f:
        testSet = pickle.load(f)
        f.close()
    testSet.plotData(ratio)

    ratio = 0.001
    with open(fileName + '_clean.pkl', "rb") as f:
        testSet2 = pickle.load(f)
        f.close()
    testSet2.plotData(ratio)
    return


def test8():
    # Vecteurs necessaires pour traiter les données
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'c': 'CS', 'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om', 'or', 'oo', '0n']
    path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\2017-08-01_test_2.3_results'

    # On itere sur tous les boucles
    for algo in algos:
        for type in types:
            set = HistorySet.HistorySet()
            for strategy in strategies:
                for instance in instances:
                    foldername = path2results + '\\' + instance + '_' + type + '\\' + algo + strategy
                    for seed in seeds:
                        historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                        filename = foldername + '\\' + historyfile
                        currentHist = NOMAD.readLog(filename)
                        set.addHistory(currentHist)

                        # Setter les bons parametres pour le set
                set.setNumberProblem(len(instances))
                set.setNumberSeed(len(seeds))
                set.setNumberStrat(1)
                set.setAlgo(algo)
                set.setProblemClass(type)

                # Nettoyer et garder seulement les succès

            for history in set.historyList:
                history.clean()

                # Pickling
            with open(algo + type + '.pkl', 'wb') as output:
                pickle.dump(set, output, pickle.HIGHEST_PROTOCOL)
                output.close()
            del set


def test9():
    # On veut plotter les rations
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'c': 'CS', 'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om', 'or', 'oo', '0n']
    ratios = [0.1, 0.01, 0.001]
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\2017-08-01_test_2.3_results\\plot_data\\'

    for algo in algos:
        for type in types:
            for ratio in ratios:
                fileName = path2file + algo + type
                with open(fileName + '.pkl', "rb") as f:
                    testSet = pickle.load(f)
                    f.close()
                testSet.plotData(ratio)
                testSet.plotPerformance(ratio)
                del testSet


def test10():
    # On veut plotter les rations mais avec le bon shnit
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'c': 'CS', 'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om', 'or', 'oo', '0n']
    ratios = [0.1, 0.01, 0.001]
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\2017-08-01_test_2.3_results\\plot_data\\'

    for algo in algos:
        for type in types:
            fileName = path2file + algo + type
            with open(fileName + '.pkl', "rb") as f:
                testSet = pickle.load(f)
                f.close()
            for ratio in ratios:
                # testSet.plotData(ratio)
                testSet.plotPerformance(ratio)
            del testSet

def test11():
    # plot data pour tester les new params
    type = 'SMOOTH'
    algo = {'c': 'CS'}
    ratio = 0.1
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\2017-08-01_test_2.3_results\\plot_data\\'
    fileName = path2file + 'c' + type
    with open(fileName + '.pkl', "rb") as f:
        testSet = pickle.load(f)
        f.close()
    testSet.plotData(ratio, True)
    del testSet

def test12():
    # On veut plotter les rations mais avec le bon shnit
    # On rajoute les logarithmes
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'c': 'CS', 'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om', 'or', 'oo', '0n']
    ratios = [0.1, 0.01, 0.001]
    logs = [True]  # ,False]
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\2017-08-01_test_2.3_results\\plot_data\\'

    for algo in algos:
        for type in types:
            fileName = path2file + algo + type
            with open(fileName + '.pkl', "rb") as f:
                testSet = pickle.load(f)
                f.close()
            for ratio in ratios:
                for log in logs:
                    testSet.plotData(ratio, log)
                    testSet.plotPerformance(ratio, log)
            del testSet

def assim_nomad(read, plot):
    # Vecteurs necessaires pour traiter les données
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NOISY3', 'WILD3', 'NONDIFF']
    # types = ['NONDIFF']

    algos = {'c':'CS','g':'GPS','m':'MADS','t':'DEFAULT'}
    opportunism = 'OG'
    # Strategies decommenter celui avec le n si
    strategies = ['n', 'ol', 'os', 'om','or','oo','0n']
    #strategies = ['oo']

    path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\MW_'+opportunism.upper()
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\plot_data\\'
    # path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\nomad_m_et_t'

    if read:
        # On itere sur tous les boucles
        for algo in algos:
            for type in types:
                current_set = HistorySet.HistorySet()
                list_for_all_hist = []
                for strategy in strategies:
                    for instance in instances:
                        for seed in seeds:
                            historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                            foldername = path2results + '\\' + instance + '_' + type + '\\' + algo + strategy
                            filename = foldername + '\\' + historyfile
                            currentHist = NOMAD.readLog_MW(filename)
                            currentHist.clean()
                            current_set.addHistory(currentHist)
                    print(' '.join([algo, type, strategy]))

                current_set.setNumberProblem(len(instances))
                current_set.setNumberSeed(len(seeds))
                current_set.setNumberStrat(1)
                current_set.setAlgo(algo)
                current_set.setProblemClass(type)

                # Pickling
                path2plot_data = path2file + algo + type + '.pkl'
                with open(path2plot_data, 'wb') as output:
                    pickle.dump(current_set, output, pickle.HIGHEST_PROTOCOL)
                    print('Pickling data for set : ' + ' '.join([algo, type, current_set.opportunism]))
                    output.close()
                del current_set

    if plot:
        # On veut plotter les rations mais avec le bon shnit
        # On rajoute les logarithmes
        ratios = [10 ** (-1),10**(-3), 10**(-5), 10 ** (-7)]
        # ratios = [0.1, 0.01, 0.001, 10**(-4), 10**(-5), 10**(-6), 10**(-7)]

        # logs = [True,False] # Pour tracer les deux styles
        logs = [True]

        # # Decommenter si on veut tracer par style
        for algo in algos:
            for type in types:
                fileName = path2file + algo + type
                with open(fileName + '.pkl', "rb") as f:
                    testSet = pickle.load(f)
                    f.close()
                    testSet.setOpportunism('OG')
                for ratio in ratios:
                    for log in logs :
                        testSet.plotData(ratio, log)
                        # testSet.plotPerformance(ratio, log)
                        print('Ploting performance and data for set : ' + ' '.join([algo, type]))
                del testSet

        # for algo in algos:
        #     amalgame = HistorySet.HistorySet()
        #     amalgame.setProblemClass('TOUS')
        #     amalgame.setAlgo(algo)
        #     for type in types:
        #         fileName = path2file + algo + type
        #         with open(fileName + '.pkl', "rb") as f:
        #             testSet = pickle.load(f)
        #             f.close()
        #         for hist in testSet.historyList:
        #             amalgame.addHistory(hist)
        #         del testSet
        #     for ratio in ratios:
        #         for log in logs:
        #             amalgame.plotData(ratio, log)
        #             amalgame.plotPerformance(ratio, log)
        #             print('Ploting performance and data for set : ' + ' '.join([algo, 'all']))
        #     del amalgame

def assim_nomad_special(read, plot, algos, opportunism):
    # Vecteurs necessaires pour traiter les données
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NOISY3', 'NONDIFF']#,'WILD3']
    # types = ['SMOOTH', 'NOISY3', 'NONDIFF','WILD3']
    # types = ['NONDIFF']
    # types = ['SMOOTH']
    # algos = {'c': 'CS'}
    # algos = {'t': 'DEFAULT'}
    # algos = {'m':'MADS','t':'NOMAD_MADS'}

    # Strategies
    strategies = ['ol', 'os', 'om', 'or', 'oo', '0n']

    # # Opportunisme , si aucun = og
    # opportunism = 'secsuc'
    # opportunism = 'mineval'


    path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\MW_' + opportunism.upper()
    path2n_results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\MW_OG'
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\plot_data\\'

    if read:
        # On itere sur tous les boucles
        for algo in algos:
            for type in types:
                current_set = HistorySet.HistorySet()
                for strategy in strategies:
                    for instance in instances:
                        for seed in seeds:
                            historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                            foldername = path2results + '\\' + instance + '_' + type + '\\' + algo + strategy
                            filename = foldername + '\\' + historyfile
                            currentHist = NOMAD.readLog_MW(filename)
                            currentHist.clean()
                            current_set.addHistory(currentHist)
                    print(' '.join([algo, type, strategy]))

                # Ajouter le sans opportunisme
                strategy = 'n'
                for instance in instances:
                    for seed in seeds:
                        historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                        foldername = path2n_results + '\\' + instance + '_' + type + '\\' + algo + strategy
                        filename = foldername + '\\' + historyfile
                        currentHist = NOMAD.readLog_MW(filename)
                        currentHist.clean()
                        current_set.addHistory(currentHist)


                current_set.setNumberProblem(len(instances))
                current_set.setNumberSeed(len(seeds))
                current_set.setNumberStrat(1)
                current_set.setAlgo(algo)
                current_set.setProblemClass(type)
                current_set.setOpportunism(opportunism)

                # Pickling
                path2plot_data = path2file + algo + type + current_set.opportunism + '.pkl'
                with open(path2plot_data, 'wb') as output:
                    pickle.dump(current_set, output, pickle.HIGHEST_PROTOCOL)
                    print('Pickling data for set : ' + ' '.join([algo, type, current_set.opportunism]))
                    output.close()
                del current_set

    if plot:
        # On veut plotter les rations mais avec le bon shnit
        # On rajoute les logarithmes
        ratios = [10**(-1),10**(-3),10**(-5), 10 ** (-7)]
        # ratios = [0.1, 0.01, 0.001, 10**(-4), 10**(-5), 10**(-6), 10**(-7)]

        # logs = [True,False] # Pour tracer les deux styles
        logs = [True]

        # # Decommenter si on veut tracer par style
        # for algo in algos:
        #     for type in types:
        #         fileName = path2file + algo + type
        #         with open(fileName + '.pkl', "rb") as f:
        #             testSet = pickle.load(f)
        #             f.close()
        #         for ratio in ratios:
        #             for log in logs :
        #                 testSet.plotData(ratio, log)
        #                 testSet.plotPerformance(ratio, log)
        #                 print('Ploting performance and data for set : ' + ' '.join([algo, type]))
        #         del testSet

        for algo in algos:
            amalgame = HistorySet.HistorySet()
            # amalgame.setProblemClass('SMOOTH')
            amalgame.setProblemClass('TOUS')
            amalgame.setAlgo(algo)
            amalgame.setOpportunism(opportunism)
            for type in types:
                if opportunism is not 'og':
                    fileName = path2file + algo + type + opportunism.upper()
                else:
                    fileName = path2file + algo + type
                with open(fileName + '.pkl', "rb") as f:
                    testSet = pickle.load(f)
                    f.close()
                for hist in testSet.historyList:
                    amalgame.addHistory(hist)
                del testSet

            for ratio in ratios:
                for log in logs:
                    amalgame.plotData(ratio, log)
                    # amalgame.plotPerformance(ratio, log) # Desactive pour pas tracer pur rien
                    print('Ploting performance and data for set : ' + ' '.join([algo, 'all', opportunism]))
            del amalgame

def assim_nomad_const(read, plot, algos, opportunism):
    # Vecteurs necessaires pour traiter les données

    type = 'CONSTRAINED'
    problems = ['CHENWANG_F2', 'CHENWANG_F3', 'CRESCENT', 'DISK', 'G2_10', 'G2_20', 'HS19', 'HS83', 'MAD6', 'MEZMONTES',
                'OPTENG_RBF', 'PENTAGON', 'PIGACHE', 'SNAKE','SPRING','TAOWANG_F2','ZHAOWANG_F5']
    seeds = [str(x + 1) for x in range(10)]
    # algos = {'c': 'CS'}
    # algos = {'t': 'DEFAULT'}
    # algos = {'m':'MADS','t':'NOMAD_MADS'}

    # Strategies
    strategies = ['ol', 'os', 'om', 'or', 'oo', '0n']

    # # Opportunisme , si aucun = og
    # opportunism = 'secsuc'
    # opportunism = 'mineval'


    path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\CONSTRAINED_' + opportunism.upper()
    path2n_results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\CONSTRAINED_OG'
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\plot_data\\'

    if read:
        # On itere sur tous les boucles
        for algo in algos:
            current_set = HistorySet.HistorySet()
            for strategy in strategies:
                for instance in problems:
                    for seed in seeds:
                        foldername = path2results + '\\' + instance + '\\' + algo + strategy
                        historyfile = instance  + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                        filename = foldername + '\\' + historyfile
                        if not os.path.isfile(filename): # Au cas ou les seed ont pas marcher
                            historyfile = instance + '_history_' + seed + '_' + algo + strategy + '.0.txt'
                            filename = foldername + '\\' + historyfile
                        currentHist = NOMAD.readLog_CON(filename)
                        currentHist.cleanConstrained()
                        current_set.addHistory(currentHist)
                    print(' '.join([instance, algo, strategy]))

            # Ajouter le sans opportunisme
            strategy = 'n'
            for instance in problems:
                for seed in seeds:
                    foldername = path2n_results + '\\' + instance + '\\' + algo + strategy
                    historyfile = instance  + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                    filename = foldername + '\\' + historyfile
                    if not os.path.isfile(filename): # Au cas ou les seed ont pas marcher
                        historyfile = instance + '_history_' + seed + '_' + algo + strategy + '.0.txt'
                        filename = foldername + '\\' + historyfile
                    currentHist = NOMAD.readLog_CON(filename)
                    currentHist.cleanConstrained()
                    current_set.addHistory(currentHist)

            current_set.setNumberSeed(len(seeds))
            current_set.setNumberStrat(len(strategies))
            current_set.setAlgo(algo)
            current_set.setOpportunism(opportunism)

            # Pickling
            path2plot_data = path2file + algo + type + current_set.opportunism + '.pkl'
            with open(path2plot_data, 'wb') as output:
                pickle.dump(current_set, output, pickle.HIGHEST_PROTOCOL)
                print('Pickling data for set : ' + ' '.join([algo, type, current_set.opportunism]))
                output.close()
            del current_set

    if plot:
        # On veut plotter les rations mais avec le bon shnit
        # On rajoute les logarithmes
        ratios = [10**(-1),10**(-3),10**(-5),10**(-7)]
        # ratios = [0.1, 0.01, 0.001, 10**(-4), 10**(-5), 10**(-6), 10**(-7)]
        # logs = [True,False] # Pour tracer les deux styles
        logs = [True,False]

        for algo in algos:
            amalgame = HistorySet.HistorySet()
            # amalgame.setProblemClass('SMOOTH')
            amalgame.setProblemClass('CONSTRAINED')
            amalgame.setAlgo(algo)
            amalgame.setOpportunism(opportunism)
            fileName = path2file + algo + type + opportunism.upper()
            with open(fileName + '.pkl', "rb") as f:
                testSet = pickle.load(f)
                f.close()
            for hist in testSet.historyList:
                amalgame.addHistory(hist)
            del testSet

            for ratio in ratios:
                for log in logs:
                    amalgame.plotData(ratio, log)
                    # amalgame.plotPerformance(ratio, log) # Desactive pour pas tracer pur rien
                    print('Ploting performance and data for set : ' + ' '.join([algo, 'all', opportunism]))
            del amalgame

def assim_hopspack(read, plot):
    # Vecteurs necessaires pour traiter les données
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    # algos = {'c':'CS'}#{'g': 'GPS'}
    algos = {'gss': 'GSS'}  # 't':'NOMAD_MADS'}
    strategies = ['ol', 'or']
    path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\HOPSPACK\\current'

    if read:
        # On itere sur tous les boucles
        for algo in algos:
            for type in types:
                current_set = HistorySet.HistorySet()
                list_for_all_hist = []
                for strategy in strategies:
                    for instance in instances:
                        for seed in seeds:
                            historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                            foldername = path2results + '\\' + instance + '_' + type + '\\' + algo + strategy
                            filename = foldername + '\\' + historyfile
                            currentHist = HOPSPACK.readLog(filename)
                            currentHist.clean()
                            current_set.addHistory(currentHist)
                    print(' '.join([algo, type, strategy]))

                current_set.setNumberProblem(len(instances))
                current_set.setNumberSeed(len(seeds))
                current_set.setNumberStrat(1)
                current_set.setAlgo(algo)
                current_set.setProblemClass(type)

                # Pickling
                with open(path2results + '\\plot_data\\' + algo + type + '.pkl', 'wb') as output:
                    pickle.dump(current_set, output, pickle.HIGHEST_PROTOCOL)
                    print('Pickling data for set : ' + ' '.join([algo, type]))
                    output.close()
                del current_set

    if plot:
        # On veut plotter les rations mais avec le bon shnit
        # On rajoute les logarithmes
        ratios = [10**(-1),10**(-3),10**(-5),10**(-7)]
        logs = [True]
        path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\HOPSPACK\\current\\plot_data\\'

        # for algo in algos:
        #     for type in types:
        #         fileName = path2file + algo + type
        #         with open(fileName + '.pkl', "rb") as f:
        #             testSet = pickle.load(f)
        #             f.close()
        #         for ratio in ratios:
        #             for log in logs:
        #                 testSet.plotData(ratio, log)
        #                 #testSet.plotPerformance(ratio, log)
        #                 print('Ploting performance and data for set : ' + ' '.join([algo, type]))
        #         del testSet

        for algo in algos:
            amalgame = HistorySet.HistorySet()
            # amalgame.setProblemClass('SMOOTH')
            amalgame.setProblemClass('TOUS')
            amalgame.setAlgo(algo)
            for type in types:
                fileName = path2file + algo + type
                with open(fileName + '.pkl', "rb") as f:
                    testSet = pickle.load(f)
                    f.close()
                for hist in testSet.historyList:
                    amalgame.addHistory(hist)
                del testSet

            for ratio in ratios:
                for log in logs:
                    amalgame.plotData(ratio, log)
                    # amalgame.plotPerformance(ratio, log) # Desactive pour pas tracer pur rien
                    print('Ploting performance and data for set : ' + ' '.join([algo, 'all']))
            del amalgame

def assim_imfil(read, plot):
    # Vecteurs necessaires pour traiter les données
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH'] # il n'y a que le type smooth pour imfil
    # types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'i': 'imfil'}
    strategies = ['ol', 'os', 'om', 'or', 'oo', 'on']
    opportunism = 'od'
    # opportunism = 'op'
    path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\MATLAB_IMFIL\\imfil'+opportunism+'_run_MW'
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\plot_data\\'
    path2n_results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\MATLAB_IMFIL\\current'

    if read:
        # On itere sur tous les boucles
        for algo in algos:
            for type in types:
                current_set = HistorySet.HistorySet()
                for strategy in strategies:
                    for instance in instances:
                        for seed in seeds:
                            historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.txt'
                            foldername = path2results + '\\' + instance + '_' + type + '\\' + strategy
                            filename = foldername + '\\' + historyfile
                            currentHist = imfil.readLog(filename)
                            currentHist.clean()
                            current_set.addHistory(currentHist)
                    print(' '.join([algo, type, strategy]))

            # On ajoute le sans opportunisme
            strategy = 'n'
            for instance in instances:
                for seed in seeds:
                    historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.txt'
                    foldername = path2n_results + '\\' + instance + '_' + type + '\\' + strategy
                    filename = foldername + '\\' + historyfile
                    currentHist = imfil.readLog(filename)
                    currentHist.clean()
                    current_set.addHistory(currentHist)

            current_set.setNumberProblem(len(instances))
            current_set.setNumberSeed(len(seeds))
            current_set.setNumberStrat(1)
            current_set.setAlgo(algo)
            current_set.setProblemClass(type)
            current_set.setOpportunism(opportunism)

            # Pickling

            path2plot_data = path2file + algo + type + opportunism + '.pkl'
            with open(path2plot_data, 'wb') as output:
                pickle.dump(current_set, output, pickle.HIGHEST_PROTOCOL)
                print('Pickling data for set : ' + ' '.join([algo, type, current_set.opportunism]))
                output.close()
            del current_set


    if plot:
        # On veut plotter les rations mais avec le bon shnit
        # On rajoute les logarithmes
        ratios = [10**(-1), 10**(-3), 10**(-5), 10**(-7)]
        logs = [True]

        ########################################
        # # Pour plotter par type
        # for algo in algos:
        #     for type in types:
        #         fileName = path2file + algo + type
        #         with open(fileName + '.pkl', "rb") as f:
        #             testSet = pickle.load(f)
        #             f.close()
        #
        #         # Si il y a un probleme avec les extensions dans le nom de la stratégie
        #         for history in testSet.historyList:
        #             imfil.fixHistStrat(history)
        #
        #         for ratio in ratios:
        #             for log in logs:
        #                 testSet.plotData(ratio, log)
        #                 testSet.plotPerformance(ratio, log)
        #                 print('Ploting performance and data for set : ' + ' '.join([algo, type]))
        #         del testSet
        ####################################################

        # Pour plotter sur tous les problèmes
        for algo in algos:
            amalgame = HistorySet.HistorySet()
            # amalgame.setProblemClass('SMOOTH')
            amalgame.setProblemClass('TOUS')
            amalgame.setAlgo(algo)
            amalgame.setOpportunism(opportunism)
            for type in types:
                fileName = path2file + algo + type + opportunism
                with open(fileName + '.pkl', "rb") as f:
                    testSet = pickle.load(f)
                    f.close()
                for hist in testSet.historyList:
                    amalgame.addHistory(hist)
                del testSet

            for ratio in ratios:
                for log in logs:
                    amalgame.plotData(ratio, log)
                    # amalgame.plotPerformance(ratio, log) # Desactive pour pas tracer pur rien
                    print('Ploting performance and data for set : ' + ' '.join([algo, 'all']))
            del amalgame

def assim_styrene(algos, strats):
    # Assimile tous les runs de styrene et les sauvegarde comme des history unique
    # Vraies params
    # probname = 'STYRENE'
    # seeds = [str(x + 1) for x in range(10)]
    # startpoints = ['X0','X1','x2','X3']
    # algos = {'c':'CS','g':'GPS','m':'MADS','t':'TRUE'}
    # strategies = ['n', 'ol', 'os', 'om','or','oo','on']

    # Params pour tester
    probname = 'STYRENE'
    seeds = [str(x + 1) for x in range(10)]
    startpoints = ['X1']
    # algos = {'t': 'TRUE'}
    # strategies = ['or', 'ol']

    # Pas le  bon path pour les vrais resultats
    path2results = "C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\STYRENE"
    for startpoint in startpoints:
        current_set = HistorySet.HistorySet()
        for algo in algos:
            current_set.setAlgo(algo)
            for strategy in strats:
                for seed in seeds:
                    historyfile = probname + '_' + startpoint + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                    foldername = path2results + '\\' + probname + '_' + startpoint + '\\' + algo + strategy
                    filename = foldername + '\\' + historyfile
                    current_history = NOMAD.readLog_singleprob(filename)
                    current_history.clean()
                    current_set.addHistory(current_history)
            current_set.setProblemClass(probname)
            current_set.plot_convergence_all_curves

def test_graphe(read, plot):
    # Vecteurs necessaires pour traiter les données
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH']
    algos = {'m': 'MADS'}
    # algos = {'m':'MADS','t':'NOMAD_MADS'}
    # strategies = ['n', 'om', 'ol','or','oo','0n','os']
    strategies = ['n', 'om', 'ol']
    # path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\nomad_m_neg'
    path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\nomad_c_et_g\\plot_data\\'
    path2results = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\nomad_m_et_t'

    if read:
        # On itere sur tous les boucles
        for algo in algos:
            for type in types:
                current_set = HistorySet.HistorySet()
                list_for_all_hist = []
                for strategy in strategies:
                    for instance in instances:
                        for seed in seeds:
                            historyfile = instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'
                            foldername = path2results + '\\' + instance + '_' + type + '\\' + algo + strategy
                            filename = foldername + '\\' + historyfile
                            currentHist = NOMAD.readLog_MW(filename)
                            currentHist.clean()
                            current_set.addHistory(currentHist)

                print(' '.join([algo, type, strategy]))

            current_set.setNumberProblem(len(instances))
            current_set.setNumberSeed(len(seeds))
            current_set.setNumberStrat(1)
            current_set.setAlgo(algo)
            current_set.setProblemClass(type)

            # Pickling
            with open('nomad_c_et_g\\plot_data\\' + algo + type + '.pkl', 'wb') as output:
                pickle.dump(current_set, output, pickle.HIGHEST_PROTOCOL)
                print('Pickling data for set : ' + ' '.join([algo, type]))
                output.close()
            del current_set

    if plot:
        # On veut plotter les rations mais avec le bon shnit
        # On rajoute les logarithmes
        ratios = [10 ** (-3), 10 ** (-7)]
        logs = [False]
        # path2file = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\nomad_m_et_t\\plot_data\\'

        for algo in algos:
            for type in types:
                fileName = path2file + algo + type
                with open(fileName + '.pkl', "rb") as f:
                    testSet = pickle.load(f)
                    f.close()
                for ratio in ratios:
                    for log in logs:
                        testSet.plotData(ratio, log)
                        # testSet.plotPerformance(ratio, log)
                        print('Ploting performance and data for set : ' + ' '.join([algo, type]))
                del testSet


# assim_styrene(['m','t'],['or','om'])
# assim_styrene(['m','t'],['n','oo'])
# assim_styrene(['m','t'],['0n','oo'])
# assim_styrene(['m','t'],['om','n'])
# assim_styrene(['m','t'],['om','oo'])
# assim_nomad(False,True)
# test_graphe(True, True)
# assim_nomad_special(True,False)
# assim_nomad_special(True,False, {'m': 'MADS'})
# assim_nomad_special(True,False, {'g': 'GPS'})
# assim_nomad_special(False, True, {'t': 'TRUE '}, 'og')
# assim_nomad_special(True,False, {'t': 'DEFAULT'},'secsuc')
# assim_nomad_special(False,True, {'c':'CS','g':'GPS','m':'MADS','t':'DEFAULT'},'')
assim_nomad_special(False,True, {'m': 'MADS'},'og')
# assim_nomad_const(False,True, {'c': 'CS','g':'GPS','m':'MADS','t':'TRUE'},'OG')
# assim_nomad_const(False,True, {'m': 'MADS'},'OG')
# assim_nomad_const(False,True, {'t': 'TRUE'},'OG')
# assim_nomad_const(False,True, {'c': 'CS','g':'GPS','m': 'MADS','t': 'TRUE'},'SECSUC')
# assim_nomad_const(False,True, {'c': 'CS','g':'GPS','m': 'MADS','t': 'TRUE'},'MINEVAL')
# assim_hopspack(False,True)
# assim_nomad_const(False,True, {'c': 'CS','g':'GPS','m':'MADS','t':'TRUE'},'OG')
# assim_nomad_const(False,True, {'c': 'CS','g':'GPS','m':'MADS'},'SECSUC')
# assim_nomad_const(False,True, {'c': 'CS','g':'GPS','m':'MADS'},'MINEVAL')
# assim_imfil(False,True)
