import os
import shutil
from subprocess import call


def edit_mw_cpp(instance, problem_index, m, n, declinaison):
    with open("src/MOREWILD/bb.cpp", 'r') as currentfile:
        # Ouvrir le history.txt
        bbcpp = currentfile.readlines()
        currentfile.close()

    instance_line = list(bbcpp[688])
    type_line = list(bbcpp[689])
    nprob_line = list(bbcpp[690])
    n_line = list(bbcpp[691])
    m_line = list(bbcpp[692])

    # on cree un dict pour iterer sur les variable a modifier
    line_dict = {instance: instance_line, declinaison: type_line, problem_index: nprob_line, n: n_line, m: m_line}

    for obj in line_dict:
        idx = 33
        for el in list(str(obj)):
            line_dict[obj][idx] = el
            idx += 1
        line_dict[obj][:] = line_dict[obj][0:idx]
        line_dict[obj].append(' ')
        line_dict[obj].append(';')
        line_dict[obj].append('\n')

    bbcpp[688] = ''.join(instance_line)
    bbcpp[689] = ''.join(type_line)
    bbcpp[690] = ''.join(nprob_line)
    bbcpp[691] = ''.join(n_line)
    bbcpp[692] = ''.join(m_line)

    # thefile = open(dir_name+"\ bb.cpp", 'w')
    dir_name = 'MOREWILD_' + declinaison + str(instance)
    thefile = open(dir_name + "/bb.cpp", 'w')
    for item in bbcpp:
        thefile.write('%s ' % item)
    thefile.close()


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class TransitionError(Error):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message


class Run:
    """Run class is a dummy class that represents any algorithm run on a problem.

    Attributes:
        problem : name of the problem, always in caps
        seed: an integer that resets the random seed or just specifies another distinct run
        x0 : start point
    """

    def __init__(self, problem, seed, x0):
        """Initialisation with all 3 attributes"""
        if problem is tuple:
            self.problem = Problem(problem[0], problem[1], problem[2])
        else:
            self.problem = Problem(problem)
        self.seed = seed
        self.x0 = x0


class NomadRun(Run):
    """ NomadRun is a child class of Run which is specific to the NOMAD solver

    Attributes :
        problem, seed and x0
        algorithm : string which algorithm of coordinate search, generalized pattern search, mesh adaptive direct search
            neg and orthomads by default is used in the run
        opportunism : string opportunistic strategy used in the run either (n)on-opportunistic, (s)imple, (p) th success
            or minimum (q) evals
        ordering : string ordering strategy used in the run, either (l)exicographic, (r)andom, (d)irection of last
            success, (m)odel-guided, (o)mniscient or (i)nverse-omniscient
        """

    def __init__(self, problem, seed, x0, algorithm, opportunism, ordering):
        """ Initialisation with inheritance from RUN and all the other needed arguments"""
        Run.__init__(self, problem, seed, x0)
        self.x0 = x0
        self.algorithm = algorithm
        self.opportunism = opportunism
        self.ordering = ordering


class Problem:
    """ Designates the underlying optimization problem

    Attributes :
        """
    def __init__(self, name, data, declinaison='undefined'):
        """ Initialized with name of problem"""

        # Nom du probleme
        self.name = name
        # Dans le cas ou c'est MOREWILD
        if self.name is tuple and self.name[0] == 'MOREWILD':
            declinaison = declinaison.upper()
            if declinaison not in ['SMOOTH', 'NONDIFF', 'NOISY3', 'WILD3']:
                InputError('Declinaison', 'Declinaison invalide')
            # Format des noms pour morewild : MOREWILD##DECLINAISON
            self.name = name[0] + name[1] + declinaison.upper()

        print 'Getting data for problem ' + self.name
        self.instance = data[0]
        self.mw_problem_index = data[1]
        self.m = data[2]
        self.ns = data[3]
        self.dim_r = data[4]
        self.dim_t = data[4]
        self.lb = data[6]
        self.ub = data[7]
        self.neb = data[8]
        self.npb = data[9]
        self.x0 = {'X0', data[10]}

        # Il faudrait une section ici pour generer d'autre
        # points de departs X1 X2 ... en option

        print 'Copying and creating bb.cpp, bb.exe for' + self.name
        if self.name[0:7] == 'MOREWILD':
            # Si il s'agit d'un probleme morewild
            # Construire l'architecture pour la blackbox
            file_path = "./" + self.name + '/X0'
            directory = os.path.dirname(file_path)
            # noinspection PyBroadException
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)
            edit_mw_cpp(self.instance, self.mw_problem_index, self.m, self.dim_r, declinaison)
        else:
            # Si il n'est pas un morewild on peut avoir plusieurs points
            # de depart et donc plusieurs fichiers
            for pt in self.x0:
                file_path = "./" + self.name +'/'+pt
                directory = os.path.dirname(file_path)
                # noinspection PyBroadException
                try:
                    os.stat(directory)
                except:
                    os.mkdir(directory)
                shutil.copy('src/'+self.name+'/bb.cpp', directory + '/bb.cpp')
                call(['g++ -o bb.exe bb.cpp'], shell=True, cwd=directory)
