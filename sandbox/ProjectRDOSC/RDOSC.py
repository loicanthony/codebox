import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help="Increase output verbosity", action='store_true')
parser.add_argument('-m', '--make', help="Will make files for selected runs", action='store_true')
parser.add_argument('-r', '--run', help="Will run selected runs", action='store_true')
parser.add_argument('runs', help='All nomenclature for runs', nargs='*')
args = parser.parse_args()
verb = args.verbose

if verb:
    print 'Verbosity on'

if verb:
    print 'Initialisation du data, necessite les fichiers algorithmdata.csv et problemdata.csv\n'

# Initialisation des listes avec le fichier algorithmdata.csv et problemdata.csb
with open('algorithmdata.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    reader = [x for x in reader]

all_solvers = reader[0]
all_opportunisms = reader[1]
all_strategies = reader[2]
default_seeds = reader[3]

with open('problemdata.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    problem_data = {(x[0] if x[0] != 'MOREWILD' else (x[0], x[1])): (x[1:] if x[0] != 'MOREWILD' else x[1:]) for x in reader}

solvers_to_run, opportunisms_to_run, strategies_to_run, seeds_to_run, problems_to_run = [], [], [], [], []
args.runs = [arg.Upper() for arg in args.runs]
# On prends les arguments arguments et on les mets dans les bonnes listes
for arg in args.runs:

    # Si c'est dans les solveurs, ca veut dire que cest un solveur
    if arg in all_solvers:
        solvers_to_run.append(arg)

    # Check opportunism
    if arg[0] in all_opportunisms and len(arg) < 3:
        opportunisms_to_run.append(arg)

    # Check ordo
    if arg in all_strategies:
        strategies_to_run.append(arg)

    if arg[-5:] == 'SEEDS':
        seeds_to_run = range(1, int(arg[0:-6]))
    else:
        seeds_to_run = default_seeds

    # if arg == 'CONSTRAINED':
        print('Ca veut dire qu''on roule tous les contraints')

    # if arg == 'MOREWILD':
        print('Ca veut dire qu''on roule tous les morewild')

if args.make:
    print 'construit les param files'

    if args.run:
        print 'roule les param files'

print args.runs
print strategies_to_run
print seeds_to_run
print opportunisms_to_run
print solvers_to_run
