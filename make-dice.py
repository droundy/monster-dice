import matplotlib
matplotlib.use('Agg')

import glob, os, string, numpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

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
    'swordsman': {
        'move': ['x','+','*','*','*','*'],
        'color': 'black',
        'armor': [0,0,0,1,1,1],
        'flies': [0]*6,
    },
    'mage': {
        'move': ['+','x','*','*','*','*'],
        'color': 'red',
        'armor': [0]*6,
        'flies': [0]*6,
    },
    'spearman': {
        'move': ['+']*6,
        'color': 'blue',
        'armor': [0]*6,
        'flies': [0]*6,
    },
    'axeman': {
        'move': ['x']*6,
        'color': 'green',
        'armor': [0]*6,
        'flies': [0]*6,
    },
    'healer': {
        'move': ['x','x','x','x','*','*'],
        'color': 'brown',
        'armor': [0]*6,
        'flies': [0]*6,
    },
    'archer': {
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

def plotheal(sz,color):
    R = sz*.275/.5
    x0 = .17
    x = np.linspace(0,R+x0,100)
    dx = x[1]-x[0]
    ytop =  np.sqrt(R**2 - (x-x0)**2) +.12
    ybot = -np.sqrt(R**2 - (x-x0)**2) +.12
    i=95
    while i >= 0:
        if ybot[i] > ybot[i+1] - dx*.7:
            ybot[i] = 2*ybot[i+1] - ybot[i+2]
        i-=1
    plt.fill_between(x,ybot,ytop, facecolor=color)
    plt.fill_between(-x,ybot,ytop, facecolor=color)

def plotwing(sz, color):
    x = np.linspace(-sz,sz,100)
    X = x/sz
    wingtop = .5*np.sin(X*np.pi/2)**2 + .3 + .1*abs(X)
    wingbot = wingtop - 0.3*np.sin(X*np.pi)**2 - .05 # *X
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
        plotheal(.4, 'red')
        plotheal(.35, directioncolor)
    if m['flies'][side-1]:
        plotwing(.9, (.8,.8,.8))
    plt.text(0,0,str(side),color=m['color'],fontsize=24,
             verticalalignment='center', horizontalalignment='center')
    text = plt.text(0, -0.8, name, color=directioncolor,
                    ha='center', va='center', size=14)
    text.set_path_effects([path_effects.Stroke(linewidth=3, foreground=m['color']),
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
