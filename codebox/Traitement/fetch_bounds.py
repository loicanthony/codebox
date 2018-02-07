import csv

# Ce script doit ete execute dans le bon folder car il doit parcourir le bon path
seed = str(1)
instances = [str(x + 1) for x in range(53)]
types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
algo = 'm'
strategy = 'om'

#Initialisation d'un array 2d numpy qui aura une ligne par combo
Table = []
# On itere sur toutes les combinaisons type / instance , ouvre le fichier et sort le pt initial et la sortie
for instance in instances:
    for type in types:
        foldername =  instance + '_' + type + '\\' + algo + strategy +'\\'
        historyfile = foldername + instance + '_' + type + '_history_' + seed + '_' + algo + strategy + '.' + seed + '.txt'

        #Ici on ouvre le fichier
        with open(historyfile, 'r') as file:
            iniFile = file.readlines()
            file.close()

        # Prends la premiere ligne
        line_1=iniFile[0]

        # Prends la derniere ligne
        line_end = iniFile[-1]

        #Splitter les lignes pour exclure les valeurs de la fonction, qui sont inutiles ici, et les avoirs en array
        list_1 = list(map(float, (line_1).split()))[0:-1]
        list_end = list(map(float, (line_end).split()))[0:-1]

        # La ligne qu'on ajoute a l'array
        line_2_append = list_1 + list_end
        line_2_append.insert(0,instance)
        line_2_append.insert(1, type)

        #Maintenant que la ligne est faite, on peut ajouter cette liste a notre table
        Table.append(line_2_append)

# Ouvre le fichier des bounds quon va creer
with open('imfil_bounds.txt','w') as myfile:
    for obj in Table:
        for obj2 in obj:
            #obj2.strip('"')
            myfile.write(str(obj2) + ' ')
        myfile.write('\n')
    myfile.close()
