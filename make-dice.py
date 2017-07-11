import matplotlib
matplotlib.use('Agg')

import glob, os, string, numpy
import numpy as np
import matplotlib.pyplot as plt

os.system('mkdir -p sides')

monsters = {
    'skeleton': {
        'move': ['x','+','*','*','*','*'],
        'color': 'black',
        'armor': [0]*6,
        'flies': [0]*6,
    },
    'dragon': {
        'move': ['+','x','*','*','*','*'],
        'color': 'red',
        'armor': [0,1,1,1,2,2],
        'flies': [0,0,0,1,1,1],
    },
    'troll': {
        'move': ['+']*6,
        'color': 'blue',
        'armor': [0,0,1,1,1,1],
        'flies': [0]*6,
    },
    'ogre': {
        'move': ['x']*6,
        'color': 'green',
        'armor': [0,0,1,1,1,1],
        'flies': [0]*6,
    },
    'griffin': {
        'move': ['x','x','x','x','x','x'],
        'color': 'brown',
        'armor': [0]*6,
        'flies': [0,0,1,1,1,1],
    },
    'basilisk': {
        'move': ['+','+','+','+','+','*'],
        'color': 'y',
        'armor': [0]*6,
        'flies': [0]*6,
    },
}


imsz = 1.25
safesz = 1.0
lw = .25

def plotshield(sz,color):
    x = np.linspace(-sz,sz,100)
    X = x/sz
    yshield = sz/.5*(.5 - .6*(np.sqrt(1-X**8)) + 0.5*(abs(X)-1))
    plt.fill_between(x,yshield,sz, facecolor=color)

def plotwing(sz, color):
    x = np.linspace(-sz,sz,100)
    X = x/sz
    wingtop = .5*np.sin(X*np.pi/2)**2 + .3 + .1*abs(X)
    wingbot = wingtop - 0.3*np.sin(X*np.pi)**2 - .05 # *X
    plt.fill_between(x,wingtop*sz/.9,wingbot*sz/.9, facecolor=color)

def plotme(m, side):
    plt.figure(figsize=(2,2))
    plt.xlim(-imsz,imsz)
    plt.ylim(-imsz,imsz)
    plt.gca().set_position([0, 0, 1, 1])
    directioncolor = 'white'
    if m['color'] in ['y']:
        directioncolor = 'black'
    plt.gca().set_facecolor(m['color'])
    if m['move'][side-1] in '*+':
        plt.fill_between(np.linspace(-imsz,imsz,3), -lw, lw, facecolor=directioncolor)
        plt.fill_between(np.linspace(-lw,lw,3), -imsz, imsz, facecolor=directioncolor)
    if m['move'][side-1] in '*x':
        x = np.linspace(-imsz,imsz,3)
        plt.fill_between(x, x-lw*np.sqrt(2), x+lw*np.sqrt(2), facecolor=directioncolor)
        plt.fill_between(x,-x-lw*np.sqrt(2),-x+lw*np.sqrt(2), facecolor=directioncolor)
    plt.text(0,0,str(side),color=m['color'],fontsize=24,
             verticalalignment='center', horizontalalignment='center')
    armor = m['armor'][side-1]
    if armor > 0:
        if armor > 1:
            plotshield(.61, 'black')
            plotshield(.6, 'gray')
        plotshield(.51, 'black')
        plotshield(.5, directioncolor)
    if m['flies'][side-1]:
        plotwing(.9, (.8,.8,.8))

for monster in monsters:
    for side in [1,2,3,4,5,6]:
        # fac.write('| xelatex {}-{}\n\n'.format(monster,side))
        plotme(monsters[monster], side)
        plt.savefig('sides/{}-{}.pdf'.format(monster,side))
        plt.savefig('sides/{}-{}.png'.format(monster,side), dpi=94)
#         with open('sides/{}-{}.tex'.format(monster,side),'w') as f:
#             f.write(r'''\documentclass[11pt]{article}

# \usepackage[paperwidth=2.25in,paperheight=2.25in,width=2in,height=2in]{geometry}

# \usepackage{tikz}
# \usepackage{xcolor}
# \usepackage{graphicx}
# \usepackage[space]{grffile}
# \usepackage{fontspec} % Needed to run XeLaTeX
# \usepackage{lmodern}

# \usetikzlibrary{shapes.geometric,circuits,shapes.gates.logic.US,shapes.arrows}

# \pagestyle{empty}
# \thispagestyle{empty}

# \begin{document}
#    \small\[
# \begin{array}{cccccc}
#     1 & 2 & 3 & 4 & 5 & 6 \\
#     x & * & + & s
#             \end{array}\]
#    %\begin{tikzpicture}[remember picture, overlay]
#    %    %\draw[fill=green] (current page.north west) rectangle (current page.south east);
#    %    %\draw[fill=red] (current page.center) circle;
#    %    \draw[dotted] (0,0) node {1st node}
#    %         -- (1,1) node {2nd node}
#    %         -- (0,-2) node {3rd node}
#    %         -- cycle;
#    %\end{tikzpicture}
# \end{document}

# ''')
