import matplotlib
matplotlib.use('Agg')

import glob, os, string, numpy, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

import dice

with open('dice_app/lib/dice.dart', 'w') as f:
    f.write('var all_monsters = {')
    for monster in dice.monsters:
        f.write('    "{}": ['.format(monster['name']))
        for m in monster['move']:
            f.write('"{}",'.format(m))
        f.write('],\n')
    f.write('};\n\n')
    f.write('var all_actions = {')
    for action in dice.actions:
        f.write('    "{}": ['.format(action['color']))
        for m in action['sides']:
            f.write('"{}",'.format(m))
        f.write('],\n')
    f.write('};\n')

pubspec = open('dice_app/pubspec.yaml', 'w');
with open('dice_app/pubspec.beginning.yaml', 'r') as f:
    pubspec.write(f.read())
pubspec.write('  assets:\n')

fac = open('.fac','w');

for monster in dice.monsters:
    fac.write('''| python3 die.py monster {}
c .pyc
'''.format(repr(json.dumps(monster, sort_keys=True))))
    for side in range(1,7):
        pubspec.write('    - {}-{}.png\n'.format(monster['name'], side) )

for c in dice.colortests:
    fac.write('''| python3 die.py colortest {}
c .pyc
'''.format(repr(repr((c,dice.colortests[c])))))

for action in dice.actions:
    fac.write('''| python3 die.py action {}
c .pyc
'''.format(repr(json.dumps(action, sort_keys=True))))
    for side in range(0,7):
        pubspec.write('    - {}-{}.png\n'.format(action['color'], side) )

for action in dice.action_descriptions:
    fac.write('''| python3 die.py action-help {}
c .pyc
'''.format(repr(json.dumps(action, sort_keys=True))))

with open('paper.tex','w') as f:
    f.write(r'''\documentclass[11pt]{article}

\usepackage{graphicx}
\usepackage{lmodern}
\usepackage{fullpage}

\begin{document}
\noindent
''')
    i = 0
    for monster in dice.monsters:
        if not (i & 1):
            f.write(r'\hspace{-0.5in}')
        for side in [1,2,3,4,5,6]:
            f.write(r'\includegraphics[width=0.625in]{{sides/{}-{}}}'
                    .format(monster['name'],side))
        if i & 1:
            f.write('\\\\\n\\vspace{-2pt}')
        i += 1
    for action in dice.actions:
        if not (i & 1):
            f.write(r'\hspace{-0.5in}')
        for side in [1,2,3,4,5,6]:
            f.write(r'\includegraphics[width=0.625in]{{sides/{}-{}}}'
                    .format(action['color'],side))
        if i & 1:
            f.write('\\\\\n\\vspace{-2pt}')
        i += 1
    f.write(r'''

    \pagebreak\noindent
    \includegraphics[width=2.0in]{{monster-help}}
    \includegraphics[width=2.0in]{{human-help}}
    \includegraphics[width=2.0in]{{action-help}} \\
    \includegraphics[width=2.0in]{{monster-action-help}}
    \includegraphics[width=2.0in]{{human-action-help}}
    \includegraphics[width=2.0in]{{more-action-help}}
\end{document}

''')
