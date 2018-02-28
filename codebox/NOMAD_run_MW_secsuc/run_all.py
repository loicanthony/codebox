from subprocess import call
import multiprocessing

def execute(s):
    print(s)
    call(['$NOMAD_HOME/bin/nomad ' + s], shell=True)
    return

seeds = [str(x+1) for x in xrange(10)]
instances = [str(x+1) for x in xrange(53)]
types = ['SMOOTH','NONDIFF','NOISY3']
algos = {'c':'CS','g':'GPS','m':'MADS','t':'TRUE'}
#strategies = ['or'] #reroule uniquement avec surrogate random
strategies = ['ol','os','om','or','oo','0n']
if 'or' in strategies:
    call(['chmod +x rdsgt.py'], shell = True)
total=strategies.__len__()*algos.__len__()*seeds.__len__()*instances.__len__()*types.__len__()
param_files = []

for instance in instances:
    for type in types:
        for algo in algos:
            for strategy in strategies:
                foldername = instance+'_'+type+'/'+algo+strategy
                for seed in seeds:
                    param_file = foldername + '/' + seed + '_param.txt'
                    param_files.append(param_file)


pool= multiprocessing.Pool(32)
a=pool.map(execute,param_files)


# for instance in instances:
#     for type in types:
#         # exename = instance+'_'+type+"/bb.exe"
#         # cppname = instance + '_' + type + "/bb.cpp"
#         # call(["g++", "-o", exename, cppname])
#
#         for algo in algos:
#             for strategy in strategies:
#                 foldername = instance+'_'+type+'/'+algo+strategy
#                 for seed in seeds:
#                     param_file=foldername+'/'+seed+'_param.txt'
#                     call(['$NOMAD_HOME/bin/nomad ' + param_file],shell=True)
#                     i=i+1
#                     print (str(i)+'/'+str(total)+' run de NOMAD de fait')
