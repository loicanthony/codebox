import os
import pickle
import copy
import shlex
from subprocess import call
import shutil


os.system("python save_settings.py")
pickle_file = open('param_file.pkl', 'rb')
param_settings = pickle.load(pickle_file)
pickle_file.close()

## Pour adapter le script rapidement pour une autre blackbox
# Nom du probleme
prob_names = ['CHENWANG_F2','CHENWANG_F3','CRESCENT','DISK','G2_10',
              'G2_20','HS19','HS83','HS114','MAD6','MEZMONTES','OPTENG_RBF',
              'PENTAGON','PIGACHE','SNAKE','SPRING','TAOWANG_F2','ZHAOWANG_F5']
# Les instances sont comme les points de depart
pts_depart = ['x0']
#pts_depart = ['x2','x3']
# Les options du script
save_settings = True
make_bb = True
make_nesgt = True
make_directories = True
generate_paramfiles = True

if save_settings:
    settings = {}

    with open('CS', 'r') as file:
        CS = file.readlines()
        settings['CS'] = CS
        file.close()

    with open('GPS', 'r') as file:
        GPS = file.readlines()
        settings['GPS'] = GPS
        file.close()

    with open('MADS', 'r') as file:
        MADS = file.readlines()
        settings['MADS'] = MADS
        file.close()

    with open('N', 'r') as file:
        N = file.readlines()
        settings['N'] = N
        file.close()

    with open('OL', 'r') as file:
        OL = file.readlines()
        settings['OL'] = OL
        file.close()

    with open('OR', 'r') as file:
        OR = file.readlines()
        settings['OR'] = OR
        file.close()

    with open('OS', 'r') as file:
        OS = file.readlines()
        settings['OS'] = OS
        file.close()

    with open('OM', 'r') as file:
        OM = file.readlines()
        settings['OM'] = OM
        file.close()

    with open('OO', 'r') as file:
        OO = file.readlines()
        settings['OO'] = OO
        file.close()

    with open('0N', 'r') as file:
        ON = file.readlines()
        settings['0N'] = ON
        file.close()

    pickle_file = open('param_file.pkl', 'wb')
    pickle.dump(settings, pickle_file, pickle.HIGHEST_PROTOCOL)
    pickle_file.close()

if make_bb:

    for problem in prob_names:
        # Compile la boite noire
        call(['g++ -o bb.exe bb.cpp'], shell=True, cwd=problem)

        # Mets la dans le root du script
        # if os.path.exists('bb.exe'):
        #     os.remove('bb.exe')
        # shutil.move('bb/bb.exe','.')

        #Claire les object file de la compilation
        # file_list = os.listdir('bb')
        # for item in file_list:
        #     if item.endswith(".o"):
        #         os.remove(os.path.join('bb', item))

if make_nesgt:

    for problem in prob_names:
    # Compile le surrogate negatif de la boite noire pour ordonnancement negatif
        call(['g++ -o nesgt.exe nesgt.cpp'], shell=True, cwd=problem)

    # Mets la dans le root du script
    # if os.path.exists('nesgt.exe'):
    #     os.remove('nesgt.exe')
    # shutil.move('nesgt/nesgt.exe','.')

    #Claire les object file de la compilation
    # file_list = os.listdir('nesgt')
    # for item in file_list:
    #     if item.endswith(".o"):
    #         os.remove(os.path.join('nesgt', item))

#if make_directories:  PAS BESOIN ICI CAR ON A DEJA LES DIRECTORIES

        # Les instances sont comme les points de depart
        # Creer un folder par instance comme pour MW
        # for problem in prob_names:
        #     for pt in pts_depart:
        #         dir_name = prob_name + '_' + pt
        #         if not os.path.exists(dir_name):
        #             os.makedirs(dir_name)
        #
        #         #On y met la black box et le nesgt
        #         shutil.copy('bb.exe',dir_name+'/bb.exe')
        #         shutil.copy('nesgt.exe',dir_name+'/nesgt.exe')

if generate_paramfiles:

    for problem in prob_names:
        seeds = ['1','2','3','4','5','6','7','8','9','10']
        algo_types = {'c': 'CS', 'g': 'GPS', 'm': 'MADS','t':'TRUE'}
        ordering_strategies = ['n','ol','os','om','or','oo','0n']

        with open(problem+"/param.txt", 'r') as file:
            # Ouvrir le param.txt
            param_base = file.readlines()
            file.close()

        table = []  # initialisation de la liste qui contient chaque ligne du fichier
        for x in param_base:
            ligne = list(map(str, (x.split())))  # creer la ligne de float
            table.append(ligne)  # ajoute a la table
        param_base = table
        ext='.txt'

        for seed in seeds:
            for algo in algo_types:
                for strat in ordering_strategies:
                    param=copy.deepcopy(param_base)
                    for ligne in param:
                        if ligne and ligne[0] == 'HISTORY_FILE':
                            typeOfFile = 'history'
                            ligne[1] = problem +'_'+typeOfFile + '_'+seed+'_'+algo+strat + ext
                        if ligne and ligne[0] == 'SEED':
                            ligne[1] = seed
                        if ligne and ligne[0] == 'x0':
                            ligne[1] = '../x0' + ext

					param.append(['OPPORTUNISTIC_MIN_EVAL','1'])
                    param.append(param_settings[algo_types[algo]])
                    param.append(param_settings[strat.upper()])
                    param.append(('HISTORY_FILE ' + problem +'_history_'+seed+'_'+algo+strat + ext + '\n').split(' '))

                    dir_name = problem
                    #lors quon a fini les modif de param
                    newFileName = dir_name + "/" + algo+strat+'/'+seed+"_"+"param.txt"

                    if not os.path.exists(dir_name + "/" + algo + strat):
                        os.mkdir(dir_name + "/" + algo + strat)

                    #if os.path.exists(dir_name + "/" + algo + strat):
                        #shutil.rmtree(dir_name + "/" + algo + strat)
                        
                    if os.path.exists(dir_name + "/" + algo + strat + '/'+"param.txt"):
                        os.remove(dir_name + "/" + algo + strat + '/'+"param.txt")

                    thefile = open(newFileName, 'w')
                    for item in param:
                        for subItem in item:
                            thefile.write('%s ' % subItem)
                        thefile.write('\n')
                    thefile.close()

                    # if os.path.exists(dir_name + "/" + algo + strat):
                    #     shutil.rmtree(dir_name + "/" + algo + strat)

                    print (problem + algo + strat + seed)
