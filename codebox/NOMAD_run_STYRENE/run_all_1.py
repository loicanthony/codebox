from subprocess import call
import multiprocessing
import time

def execute(s):
    print(s)
    call(['$NOMAD_HOME/bin/nomad ' + s], shell=True)
    return

seeds = [str(x) for x in range(1,11)]
prob_name = 'STYRENE'
pts_depart = ['x0','x1']
#pts_depart = ['x2','x3']
#algos = {'c':'CS'} #on roule juste CS avec le mesh de 0
#algos = {'c':'CS','g':'GPS','m':'MADS'}
algos = {'c':'CS','g':'GPS','m':'MADS','t':'TRUE'}
#strategies = ['n'] #reroule uniquement avec n
strategies = ['n','ol','os','om','or','oo','0n']
if 'or' in strategies:
	call(['chmod +x rdsgt.py'], shell = True)

param_files = []

for pt in pts_depart:
	for algo in algos:
	    for strategy in strategies:
		foldername = prob_name+'_'+pt+'/'+algo+strategy
		for seed in seeds:
		    param_file = foldername + '/' + seed + '_param.txt'
		    param_files.append(param_file)

pool= multiprocessing.Pool(32)
a=pool.map(execute,param_files)
