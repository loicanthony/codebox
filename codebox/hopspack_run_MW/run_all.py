from subprocess import call
import multiprocessing


def execute(s):
    print(s)
    splitted = s.split('/')
    workingDirectory = splitted[0] + '/' + splitted[1]
    call(['./HOPSPACK_main_serial ' + splitted[2]], shell=True, cwd=workingDirectory)
    return


def clean(s):
    print s + ' is being cleaned\n'
    # On ouvre la cache creee par Hopspack
    oldCacheFile = open(s, 'r')
    oldCacheText = oldCacheFile.readlines()
    oldCacheFile.close()

    # On mets la ligne comme on la veut
    newHistoryText = []
    for line in oldCacheText:
        line = line.replace('=[', ',')
        line = line.replace(']', ',')
        line = line.split(',')
        line = [el.strip() for el in line]
        line = ' '.join([line[1], line[3] + '\n'])
        newHistoryText.append(line)

    newHistoryFile = open(s, 'w')
    for line in newHistoryText:
        newHistoryFile.write('%s' % line)
    newHistoryFile.close()


if __name__ == "__main__":
    seeds = [str(x + 1) for x in xrange(10)]
    instances = [str(x + 1) for x in xrange(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'gss': 'GSS'}
    # strategies = ['or'] #reroule uniquement avec surrogate random
    strategies = ['ol', 'or']

    total = strategies.__len__() * algos.__len__() * seeds.__len__() * instances.__len__() * types.__len__()
    paramFiles = []
    historyFiles = []

    for instance in instances:
        for type in types:
            for algo in algos:
                for strategy in strategies:
                    foldername = instance + '_' + type + '/' + algo + strategy
                    for seed in seeds:
                        paramFile = foldername + '/' + seed + '_param.txt'
                        paramFiles.append(paramFile)
                        historyFileString = '_'.join(
                            [str(instance), type, 'history', str(seed), algo + strategy + '.' + str(seed) + '.txt'])
                        historyFileName = foldername + '/' + historyFileString
                        historyFiles.append(historyFileName)

    # Run all hopspack
    pool = multiprocessing.Pool(32)
    a = pool.map(execute, paramFiles)

    # Clean all histories
    pool2 = multiprocessing.Pool(32)
    b = pool.map(clean, historyFiles)
