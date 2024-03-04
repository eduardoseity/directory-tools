import argparse
import sys
from DirectoryTools import DirectoryTools

d_tools = DirectoryTools()

parser = argparse.ArgumentParser(
    prog="Directory Tools",
)

parser.add_argument('-lf','--loadfile',nargs=1,action='append')
parser.add_argument('-lp','--loadpath',nargs=1,action='append')
parser.add_argument('-o','--output',const='',nargs='?')
parser.add_argument('-es1','--exportslot1',const='',nargs='?')
parser.add_argument('-es2','--exportslot2',const='',nargs='?')

# Check slot 1 and slot 2
loaded = []
for arg in sys.argv:
    if len(loaded) > 2:
        print(f'Too much {arg} argument. Maximum 2 -lf or -lp is permitted.')
        exit()
    if arg == '-lf' or arg == '--loadfile':
        arg = 'loadfile'
        loaded.append(arg)
    elif arg == '-lp' or arg == '--loadpath':
        arg = 'loadpath'
        loaded.append(arg)

# Load slots
if len(loaded) == 0:
    print('You need to use at list 1 -lf or -lp argument')
elif len(loaded) == 1:
    d_tools.load_slot(1,loaded[0],parser.parse_args().__dict__[loaded[0]][0][0])
elif len(loaded) == 2:
    if loaded[0] == loaded[1]:
        d_tools.load_slot(1,loaded[0], parser.parse_args().__dict__[loaded[0]][0][0])
        d_tools.load_slot(2,loaded[1], parser.parse_args().__dict__[loaded[1]][1][0])
    else:
        d_tools.load_slot(1,loaded[0], parser.parse_args().__dict__[loaded[0]][0][0])
        d_tools.load_slot(2,loaded[1], parser.parse_args().__dict__[loaded[1]][0][0])

# Compare
d_tools.compare()

# Export comparison
if parser.parse_args().output or parser.parse_args().output == '':
    output = None if parser.parse_args().output == '' else parser.parse_args().output
    d_tools.export_comparison(output)

# Export slots
if parser.parse_args().exportslot1 or parser.parse_args().exportslot1 == '':
    output = None if parser.parse_args().exportslot1 == '' else parser.parse_args().exportslot1
    d_tools.export_slot(1,output)
if parser.parse_args().exportslot2 or parser.parse_args().exportslot2 == '':
    output = None if parser.parse_args().exportslot2 == '' else parser.parse_args().exportslot2
    d_tools.export_slot(2,output)

d_tools.info()
d_tools.print()