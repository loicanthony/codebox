import os
import subprocess
import shlex
import numpy as np
import copy


class  marde:
    def __init__(self,a):
        self.value = a
    def __str__(self):
        return str(self.value)

# List et dict necessaire pour iterer sur tout
algos = {'gss':'GSS'}
prob_type_list = ['SMOOTH','NONDIFF','WILD3','NOISY3']
strategies = ['ol','or']
seeds = [str(x+1) for x in xrange(10)]
instances = [str(x+1) for x in xrange(53)]

# Ouverture des parametres sur chaque probleme
with open('prob_style.txt', 'r') as f:
    iniFile = f.readlines()
    f.close()
for place, element in enumerate(iniFile):
    element = [element.split()[1][:-1],element.split()[4][:-1],element.split()[7][:-1],element.split()[10][:-1],element.split()[13][:-1]]
    iniFile[place]=element
    for idx, num in enumerate(element):
        num = int(num)
        element[idx]=num


# Ouvrir le model de fichier de parametres
with open('exemple_params.txt', 'r') as g:
    paramModelList = g.readlines()
    g.close()
uselessList = []
for x in paramModelList:
    # Pour chaque ligne de mon history je dois
    # creer une liste
    # appender la liste a l indice x du array
    ligne = list(map(str, (x.split())))  # creer la ligne de float
    uselessList.append(ligne)  # ajoute a la table
paramModelList = uselessList

with open("bb.cpp", 'r') as file:
    # Ouvrir le history.txt
    bbcpp = file.readlines()
    file.close()

# Changer ici ce qu'on veut accomplir en roulant le script
make_directories = True
generate_bbcpp = True
generate_paramfiles = True
compile_bbcpp = True

# Boucle de creation des bb.exe et des fichiers
for type in prob_type_list:
    for object in iniFile:

        #On creer la liste des probleme
        num_inst=int(object[0])
        prob_type=marde(type)
        instance = marde(iniFile[num_inst-1][0])
        nprob = marde(iniFile[num_inst-1][1])
        n = marde(iniFile[num_inst-1][2])
        m = marde(iniFile[num_inst-1][3])
        ns = marde(iniFile[num_inst-1][4])
        dir_name = str(instance.value)+ "_" + str(prob_type.value)
        budget = n.value * 1000

        if make_directories:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

        if generate_bbcpp:

            instance_line = list(bbcpp[688])
            type_line= list(bbcpp[689])
            nprob_line = list(bbcpp[690])
            n_line = list(bbcpp[691])
            m_line = list(bbcpp[692])
            i=1

            ## on cree un dict pour iterer sur les variable a modifier
            line_dict={instance:instance_line,prob_type:type_line,nprob:nprob_line,n:n_line,m:m_line}

            for obj in line_dict:
                idx = 33
                for el in list(str(obj)):
                    line_dict[obj][idx]= el
                    idx = idx + 1
                line_dict[obj][:]=line_dict[obj][0:idx]
                line_dict[obj].append(' ')
                line_dict[obj].append(';')
                line_dict[obj].append('\n')


            # On creer une copie de bbcpp et on la modifie avant de lecrire dans un fichier
            currentBbcpp = bbcpp
            currentBbcpp[688] = ''.join(instance_line)
            currentBbcpp[689] = ''.join(type_line)
            currentBbcpp[690] = ''.join(nprob_line)
            currentBbcpp[691] = ''.join(n_line)
            currentBbcpp[692] = ''.join(m_line)

            thefile = open(dir_name+"/bb.cpp", 'w')
            for item in bbcpp:
                    thefile.write('%s ' % item)
            thefile.close()


        if compile_bbcpp == True:
            exename = dir_name + "/bb.exe"
            cppname = dir_name + "/bb.cpp"
            args=shlex.split("g++ -o " + exename +" "+ cppname)
            subprocess.Popen(args)

        if generate_paramfiles:
            for algo in algos:
                for strat in strategies:

                    # Creer le folder si necessaire
                    if make_directories:
                        if not os.path.exists(dir_name+'/'+algo+strat):
                            os.makedirs(dir_name+'/'+algo+strat)

                        # On doit copier bb.py et hopspack dans le dir inst_type/algostrat
                        bbpyOrigin = "bb.py"
                        hopspackOrigin = "HOPSPACK_main_serial"
                        bbpyDestination = dir_name+'/'+algo+strat + "/bb.py"
                        hopspackDestination = dir_name+'/'+algo+strat
                        args = shlex.split("cp " + bbpyOrigin + " " + bbpyDestination)
                        subprocess.Popen(args)
                        args = shlex.split("cp " + hopspackOrigin + " " + hopspackDestination)
                        subprocess.Popen(args)

                    # Point de depart
                    generation = "./generate_x0.exe " + str(instance.value)
                    args = shlex.split(generation)
                    x0 = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0][:-2]

                    # Itere sur toute les combinaison possibles pour creer des param files
                    for seed in seeds:
                        currentParamList = copy.deepcopy(paramModelList)
                        for line in currentParamList:

                            if line and line[0] == '"Initial' and line[1] == 'X"':
                                line[3] = str(n)
                                line[4] = x0
                                if line[5] : line[5:] = ''

                            if line and line[0] == '"Number' and line[1] == 'Unknowns"':
                                line[3] = str(n)

                            if line and line[0] == '"Scaling"':
                                line[2] = str(n)
                                #vecScaling = ' '.join([str(elem) for elem in list((np.array(x0).astype('float') / 10))])
                                x0Array = np.abs(np.array(list(x0.split())).astype('float')) / 10
                                for i in range(len(x0Array)):
                                    if x0Array[i]==0:
                                        x0Array[i]=max(x0Array[x0Array>0])
                                vecScaling =' '.join([str(elem) for elem in  list(x0Array)])
                                line[3] = vecScaling
                                line[4:] = ''

                            if line and line[0] == '"Maximum' and line[1] == 'Evaluations"':
                                line[3] = str(budget)

                            if line and line[0] == '"Cache' and line[1] == 'Output' and line[2] == 'File"':
                                cacheOutName = '_'.join(
                                    [dir_name, 'history', str(seed), algo + strat + '.' + str(seed) + '.txt'])
                                line[4] = '"' + cacheOutName + '"'

                            if line and line[0] == '"Use':
                                if strat == 'ol':
                                    line[4] = 'false'
                                else:
                                    line[4] = 'true'

                        # Quand on a fini d ecrire notre ficher
                        newFileName = dir_name + "/" + algo + strat + '/' + seed + "_" + "param.txt"
                        if os.path.exists(newFileName):
                            os.remove(newFileName)
                        newParamFile = open(newFileName, 'w')
                        for item in currentParamList:
                            for subItem in item:
                                newParamFile.write('%s ' % subItem)
                            newParamFile.write('\n')
                        newParamFile.close()
                        print (str(num_inst) + type + algo + strat + seed)


