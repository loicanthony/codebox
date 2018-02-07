#!/usr/bin/python

import sys
import random
import os

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

# Determiner l'argument donne en entre
# arglist = str(sys.argv)
iHFileName = sys.argv[1]
tag = iHFileName[6:-2]


with open(iHFileName, 'r') as f:
    # Ouvrir le input.txt
    fileContent = f.readlines()
    f.close()

# Enleve les backslash n
fileContent = [line.rstrip() for line in fileContent]

#print 'Contenu du fichier', fileContent
#print 'Tag',tag

#On determine notre point
point = " ".join([str(float(x_i)) for x_i in fileContent[2:]])

#print 'Point',point

# On mets un nom random pour etre sur que il ny a pas de probleme lors de la generation des fichiers
obFileName=str(int(10e15*random.random())) + '.txt'

# Ecrit le point dans un fichier
with open(obFileName,'w') as bbfile:
    bbfile.write(point)
    bbfile.close()

# Appel a la vrai fonction avec le point
#realBbOutput = subprocess.Popen(['./bb.exe ',obFileName], shell=True, stdout=subprocess.PIPE).stdout.read()
realBbOutput = os.popen('../bb.exe ' + obFileName).read()
convBbOutput = str(realBbOutput).rstrip()
#print convBbOutput

# Supprime le fichier
os.remove(obFileName)

# Ecrit le fichier de sortie
oHFileName = 'output.' + str(tag) + '_F'
with open(oHFileName,'w') as outfile:
    outfile.write('1\n')
    outfile.write(convBbOutput)
    outfile.write('\n0\n0')
    outfile.close()
