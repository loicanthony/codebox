import pickle

settings={}

with open('CS','r') as file:
    CS=file.readlines()
    settings['CS']=CS
    file.close()

with open('GPS','r') as file:
    GPS=file.readlines()
    settings['GPS'] = GPS
    file.close()

with open('MADS','r') as file:
    MADS=file.readlines()
    settings['MADS'] = MADS
    file.close()

with open('TRUE','r') as file:
    TRUE=file.readlines()
    settings['TRUE'] = TRUE
    file.close()

with open('N','r') as file:
    N=file.readlines()
    settings['N'] = N
    file.close()

with open('OL','r') as file:
    OL=file.readlines()
    settings['OL'] = OL
    file.close()

with open('OR','r') as file:
    OR=file.readlines()
    settings['OR'] = OR
    file.close()

with open('OS','r') as file:
    OS=file.readlines()
    settings['OS'] = OS
    file.close()

with open('OM','r') as file:
    OM=file.readlines()
    settings['OM'] = OM
    file.close()

with open('OO','r') as file:
    OO=file.readlines()
    settings['OO'] = OO
    file.close()

with open('0N','r') as file:
    ON=file.readlines()
    settings['0N'] = ON
    file.close()


pickle_file = open('param_file.pkl','wb')
pickle.dump(settings,pickle_file,pickle.HIGHEST_PROTOCOL)
pickle_file.close()
