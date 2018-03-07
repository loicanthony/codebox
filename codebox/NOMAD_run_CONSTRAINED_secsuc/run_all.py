from subprocess import call
import multiprocessing

def execute(s):
    print(s)
    call(['$NOMAD_HOME/bin/nomad ' + s], shell=True)
    return


seeds = [str(x) for x in range(1, 11)]
prob_names = ['CHENWANG_F2','CHENWANG_F3','CRESCENT','DISK','G2_10',
              'G2_20','HS19','HS83','HS114','MAD6','MEZMONTES','OPTENG_RBF',
              'PENTAGON','PIGACHE','SNAKE','SPRING','TAOWANG_F2','ZHAOWANG_F5']
pts_depart = ['x0']
algos = {'c': 'CS', 'g': 'GPS', 'm': 'MADS', 't': 'TRUE'}
strategies = ['ol', 'os', 'om', 'or', 'oo', '0n']
if 'or' in strategies:
    call(['chmod +x rdsgt.py'], shell=True)

param_files = []
for problem in prob_names:
    for algo in algos:
        for strategy in strategies:
            foldername = problem + '/' + algo + strategy
            for seed in seeds:
                param_file = foldername + '/' + seed + '_param.txt'
                param_files.append(param_file)

pool = multiprocessing.Pool(32)
a = pool.map(execute, param_files)
