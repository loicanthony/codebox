import os, os.path

#print os.listdir('.')

#print len([name for name in os.listdir('.') if os.path.isdir(name)])


for i in os.listdir('.'):
    if os.path.isdir(i):
        DIR1 = './' + i
        #print os.listdir(DIR1)
        dir_list = (j for j in os.listdir(DIR1) if '.' not in j)
        for k in dir_list:
            DIR2 = DIR1 + '/' + k
            ab=os.listdir(DIR2)
            if (len([j for j in os.listdir(DIR2) if os.path.isfile(os.path.join(DIR2, j))])) == 40:
                print DIR2

        #print str(i) + " is a directory with " + str(len([j for j in os.listdir('./'+i) if os.path.isdir(os.path.join(DIR,j))]))
