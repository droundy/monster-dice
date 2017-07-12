import matplotlib
matplotlib.use('Agg')

import glob, os, string, numpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

os.system('mkdir -p sides')

blank = {
    'move': ['x','x','x','x','*','*'],
    'color': 'brown',
    'armor': [0]*6,
    'flies': [0]*6,
    'range': [0]*6,
    'retaliate': [0]*6,
}

monsters = {
    'skeleton': {**blank,
        'move': ['x','+','*','*','*','*'],
        'color': 'black',
    },
    'dragon': {**blank,
        'move': ['+','x','*','*','*','*'],
        'color': 'red',
        'armor': [0,1,1,1,2,2],
        'flies': [0,0,0,1,1,1],
        'range': [1,1,1,1,1,1],
    },
    'troll': {**blank,
        'move': ['+']*6,
        'color': 'blue',
        'armor': [0,0,1,1,1,1],
    },
    'ogre': {**blank,
        'move': ['x']*6,
        'color': 'green',
        'armor': [0,0,1,1,1,1],
    },
    'griffin': {**blank,
        'move': ['x','x','x','x','x','x'],
        'color': 'brown',
        'flies': [0,0,1,1,1,1],
    },
    'basilisk': {**blank,
        'move': ['+','+','+','+','+','*'],
        'color': 'y',
        'range': [1,1,1,1,1,1],
    },
    'swordsman': {**blank,
        'move': ['x','+','*','*','*','*'],
        'color': 'black',
        'armor': [0,0,0,1,1,1],
    },
    'mage': {**blank,
        'move': ['+','x','*','*','*','*'],
        'color': 'red',
        'range': [1,1,1,1,1,1],
    },
    'spearman': {**blank,
        'move': ['+']*6,
        'color': 'blue',
        'retaliate': [1,1,1,1,1,1],
    },
    'axeman': {**blank,
        'move': ['x']*6,
        'color': 'green',
    },
    'healer': {**blank,
        'move': ['x','x','x','x','*','*'],
        'color': 'brown',
    },
    'archer': {**blank,
        'move': ['+','+','+','+','+','*'],
        'color': 'y',
        'range': [1,1,1,1,1,1],
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

def plotheal(sz,color):
    R = sz*.275/.5
    x0 = .13
    x = np.linspace(0,R+x0,100)
    dx = x[1]-x[0]
    ytop =  np.sqrt(R**2 - (x-x0)**2) +.12+.5
    ybot = -np.sqrt(R**2 - (x-x0)**2) +.12+.5
    i=95
    while i >= 0:
        if ybot[i] > ybot[i+1] - dx*.7:
            ybot[i] = 2*ybot[i+1] - ybot[i+2]
        i-=1
    plt.fill_between(.0+x,ybot,ytop, facecolor=color)
    plt.fill_between(.0-x,ybot,ytop, facecolor=color)

def plotrange(sz,color):
    R = sz*.275/.5
    x0 = .5
    x = np.linspace(x0-R,R+x0,100)
    dx = x[1]-x[0]
    ytop =  np.sqrt(R**2 - (x-x0)**2) -.5
    ybot = -np.sqrt(R**2 - (x-x0)**2) -.5
    plt.fill_between(x,ybot,ytop, facecolor=color)

def plotwing(sz, color):
    x = np.linspace(-sz,sz,100)
    X = x/sz
    wingtop = .3*np.sin(X*np.pi/2)**2 + .5 + .1*abs(X)
    wingbot = wingtop - 0.2*np.sin(X*np.pi)**2 - .05 # *X
    plt.fill_between(x,wingtop*sz/.9,wingbot*sz/.9, facecolor=color)

def plotretaliate(sz, color):
    x = np.linspace(-sz,sz,100)
    X = x/sz
    wingtop = .3*np.sin(X*np.pi/2)**2 + .5 + .1*abs(X)
    wingbot = wingtop - 0.2*np.sin(X*np.pi)**2 - .05 # *X
    plt.fill_between(x,wingtop*sz/.9,wingbot*sz/.9, facecolor=color)

def plotme(m, name, side):
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
    if name == 'healer' and side > 1:
        plotheal(.35, 'red')
        plotheal(.3, directioncolor)
    if m['range'][side-1]:
        plotrange(.4, 'red')
        plotrange(.3, 'white')
        plotrange(.2, 'red')
        plotrange(.1, 'white')
    if m['flies'][side-1]:
        plotwing(.9, (.8,.8,.8))
    plt.text(0,0,str(side),color=m['color'],fontsize=24,
             verticalalignment='center', horizontalalignment='center')
    text = plt.text(0, -0.8, name, color=directioncolor,
                    ha='center', va='center', size=14)
    text.set_path_effects([path_effects.Stroke(linewidth=1.5, foreground=m['color']),
                           path_effects.Normal()])
for monster in monsters:
    for side in [1,2,3,4,5,6]:
        # fac.write('| xelatex {}-{}\n\n'.format(monster,side))
        plotme(monsters[monster], monster, side)
        plt.savefig('sides/{}-{}.pdf'.format(monster,side))
        plt.savefig('sides/{}-{}.png'.format(monster,side), dpi=94)


with open('paper.tex'.format(monster,side),'w') as f:
    f.write(r'''\documentclass[11pt]{article}

\usepackage{graphicx}
\usepackage{lmodern}

\begin{document}
\noindent
''')
    for monster in monsters:
        for side in [1,2,3,4,5,6]:
            f.write(r'\includegraphics[width=0.5in]{{sides/{}-{}}}'.format(monster,side))
        f.write('\\\\\n')
    f.write(r'''
\end{document}

''')
