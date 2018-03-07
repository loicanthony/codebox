import pickle
path1 = 'C:\\Users\\Loic\\Documents\\RDOSC\\Executions\\NOMAD\\nomad_m_et_t\\'
# Ouvrir le history.txt
solutions = {}
for i in [str(x + 1) for x in range(53)]:
    path = path1 + i + '_SMOOTH\\too\\'+i+'_SMOOTH_history_1_too.1.txt'
    with open(path, 'r') as file:
        iniFile = file.readlines()
        file.close()
    last_sol = iniFile[-1] #nombre de lignes dans le fichier
    ligne = list(map(float, (last_sol).split()))[:-1]  # creer la ligne de float
    solutions[i] = ligne

pickle.dump(solutions, open( "data_sol.p", "wb" ),protocol = 2)
