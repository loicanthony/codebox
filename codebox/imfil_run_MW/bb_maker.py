#!/usr/bin/python
import os
import subprocess
import pickle
import copy
import shlex
import sys

class  marde:
    def __init__(self,a):
        self.value = a
    def __str__(self):
        return str(self.value)

prob_type = marde(sys.argv[2])
num_inst = int(sys.argv[1])

strategies = ['or','om','on','oo','ol','os','n']

with open('prob_style.txt', 'r') as f:
    # Ouvrir le parameters.txt
    iniFile = f.readlines()
    f.close()

# element = [instance, nprob, n, m, ns]
for place, element in enumerate(iniFile):
    element = [element.split()[1][:-1],element.split()[4][:-1],element.split()[7][:-1],element.split()[10][:-1],element.split()[13][:-1]]
    iniFile[place]=element
    for idx, num in enumerate(element):
        num = int(num)
        element[idx]=num

make_directories = False
generate_bbcpp = True


instance = marde(iniFile[num_inst-1][0])
nprob = marde(iniFile[num_inst-1][1])
n = marde(iniFile[num_inst-1][2])
m = marde(iniFile[num_inst-1][3])
ns = marde(iniFile[num_inst-1][4])
dir_name = "results/"+str(instance.value)+ "_" + str(prob_type.value)

if make_directories:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        for strat in strategies:
            os.makedirs(dir_name+'/'+strat)
if generate_bbcpp:
    with open("bb.cpp", 'r') as file:
        # Ouvrir le history.txt
        bbcpp = file.readlines()
        file.close()

    instance_line = list(bbcpp[688])
    type_line= list(bbcpp[689])
    nprob_line = list(bbcpp[690])
    n_line = list(bbcpp[691])
    m_line = list(bbcpp[692])
    i=1

    ## on cree un dict pour iterer sur les variable a modifier
    line_dict={instance:instance_line,prob_type:type_line,nprob:nprob_line,n:n_line,m:m_line}

    for obj in line_dict:
        for index, cara in enumerate(line_dict[obj]):
            if cara == '=':
                idx = index + 1
                for el in list(str(obj)):
                    line_dict[obj][idx]= el
                    idx = idx + 1
        line_dict[obj][:] = line_dict[obj][0:idx]
        line_dict[obj].append(' ')
        line_dict[obj].append(';')
        line_dict[obj].append('\n')

    bbcpp[688] = ''.join(instance_line)
    bbcpp[689] = ''.join(type_line)
    bbcpp[690] = ''.join(nprob_line)
    bbcpp[691] = ''.join(n_line)
    bbcpp[692] = ''.join(m_line)

    #thefile = open(dir_name+"\ bb.cpp", 'w')
    thefile = open("bb.cpp", 'w')
    for item in bbcpp:
            thefile.write('%s ' % item)
    thefile.close()
    exename = "bb.exe"
    cppname = "bb.cpp"
    args=shlex.split("g++ -o " + exename +" "+ cppname)
    subprocess.Popen(args)
# n_instance
# n
# m
# prob type
