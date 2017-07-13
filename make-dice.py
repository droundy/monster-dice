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

monsters = [
    {**blank,
     'name': 'orc',
     'move': ['x','+','*','*','*','*'],
     'color': 'black',
    },
    {**blank,
     'name': 'dragon',
     'move': ['+','x','*','*','*','*'],
     'color': 'red',
     'armor': [0,1,1,1,2,2],
     'flies': [0,0,0,1,1,1],
     'range': [1,1,1,1,1,1],
    },
    {**blank,
     'name': 'troll',
     'move': ['+']*6,
     'color': 'blue',
     'armor': [0,0,1,1,1,1],
    },
    {**blank,
     'name': 'ogre',
     'move': ['x']*6,
     'color': 'green',
     'armor': [0,0,1,1,1,1],
    },
    {**blank,
     'name': 'griffin',
     'move': ['x','x','x','x','x','x'],
     'color': 'brown',
     'flies': [0,0,1,1,1,1],
    },
    {**blank,
     'name': 'basilisk',
     'move': ['+','+','+','+','+','*'],
     'color': 'y',
     'range': [1,1,1,1,1,1],
    },
    {**blank,
     'name': 'swordsman',
     'move': ['x','+','*','*','*','*'],
     'color': 'black',
     'armor': [0,0,0,1,1,1],
     'retaliate': [1,1,1,1,1,1],
    },
    {**blank,
     'name': 'mage',
     'move': ['+','x','*','*','*','*'],
     'color': 'red',
     'range': [1,1,1,1,1,1],
    },
    {**blank,
     'name': 'spearman',
     'move': ['+']*6,
     'color': 'blue',
     'retaliate': [1,1,1,1,1,1],
    },
    {**blank,
     'name': 'axeman',
     'move': ['x']*6,
     'color': 'green',
    },
    {**blank,
     'name': 'healer',
     'move': ['x','x','x','x','*','*'],
     'color': 'brown',
    },
    {**blank,
     'name': 'archer',
     'move': ['+','+','+','+','+','*'],
     'color': 'y',
     'range': [1,1,1,1,1,1],
    },
]


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

def plotwing(sz, x0, y0, color):
    x = np.linspace(-sz,sz,100)
    X = abs(x/sz)
    wingtop = y0 + 0.8*(1 + 4*X - np.sqrt((4*X)**2 + 1))
    wingbot = wingtop - 0.3*(.2+X)*np.sqrt(1-X)
    plt.fill_between(1.1*x+x0,wingtop*sz,wingbot*sz, facecolor=color)
    plt.fill_between(.9*x+x0,.8*wingtop*sz,.8*wingbot*sz, facecolor=color)
    plt.fill_between(.8*x+x0,.65*wingtop*sz,.65*wingbot*sz, facecolor=color)

def plotretaliate(sz, color):
    theta = np.linspace(0, 0.8*2*np.pi, 200)
    r = np.zeros_like(theta) + sz/2
    plt.plot(r*np.cos(theta), r*np.sin(theta), '-', color=color, lw=3)
    theta = np.linspace(0.7*2*np.pi, 0.8*2*np.pi, 50)
    r = sz/2*(1 + (theta/theta.max()-1)*3)
    plt.plot(r*np.cos(theta), r*np.sin(theta), '-', color=color, lw=3)
    theta = np.linspace(0.71*2*np.pi, 0.8*2*np.pi, 50)
    r = sz/2*(1 - (theta/theta.max()-1)*3)
    plt.plot(r*np.cos(theta), r*np.sin(theta), '-', color=color, lw=3)

def plotpow(sz, x, y):
    theta = np.linspace(0, 2*np.pi, 21)
    r = np.zeros_like(theta) + sz/2
    r[::2] /= 2;
    plt.plot(x+.6*r*np.cos(theta), y+.6*r*np.sin(theta), '-', color=(1,1,0))
    plt.plot(x+.8*r*np.cos(theta), y+.8*r*np.sin(theta), '-', color='orange')
    plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), 'r-')

def plotteleport(sz, x, y):
    theta = np.linspace(0, 2*np.pi, 201)
    r = np.zeros_like(theta)+sz/5
    plt.plot(x+sz/2+r*np.cos(theta),y+r*np.sin(theta), '-', color='white')
    plt.plot(x-sz/2+r*np.cos(theta),y+r*np.sin(theta), '-', color='white')
    plt.plot(x+sz/2+r*np.cos(theta),y+r*np.sin(theta), 'k:')
    plt.plot(x-sz/2+r*np.cos(theta),y+r*np.sin(theta), 'k:')
    X = np.linspace(x-sz/2,x+sz/2,10)
    Y = np.zeros_like(X)+y
    plt.plot(X, Y, 'k-')
    X = np.linspace(x+sz/4,x+sz/2,10)
    Y = y + (X-(x+sz/2))
    plt.plot(X, Y, 'k-')
    X = np.linspace(x+sz/4,x+sz/2,10)
    Y = y - (X-(x+sz/2))
    plt.plot(X, Y, 'k-')

def plotme(m, side):
    name = m['name']
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
    if name == 'mage' and side > 2:
        plotpow(.6, -.5, -.5)
        plotteleport(.6, 0, .55)
    if m['range'][side-1]:
        plotrange(.4, 'red')
        plotrange(.3, 'white')
        plotrange(.2, 'red')
        plotrange(.1, 'white')
    if m['flies'][side-1]:
        plotwing(.9, 0, 0.3, (.8,.8,.6))
    if m['retaliate'][side-1]:
        plotretaliate(.6, 'red')
    plt.text(0,0,str(side),color=m['color'],fontsize=24,
             verticalalignment='center', horizontalalignment='center')
    text = plt.text(0, -0.8, name, color=directioncolor,
                    ha='center', va='center', size=14)
    text.set_path_effects([path_effects.Stroke(linewidth=1.5, foreground=m['color']),
                           path_effects.Normal()])
for monster in monsters:
    for side in [1,2,3,4,5,6]:
        # fac.write('| xelatex {}-{}\n\n'.format(monster,side))
        plotme(monster, side)
        plt.savefig('sides/{}-{}.pdf'.format(monster['name'],side))
        plt.savefig('sides/{}-{}.png'.format(monster['name'],side), dpi=94)


with open('paper.tex'.format(monster,side),'w') as f:
    f.write(r'''\documentclass[11pt]{article}

\usepackage{graphicx}
\usepackage{lmodern}

\begin{document}
\noindent
''')
    for monster in monsters:
        for side in [1,2,3,4,5,6]:
            f.write(r'\includegraphics[width=0.5in]{{sides/{}-{}}}'
                    .format(monster['name'],side))
        f.write('\\\\\n')
    f.write(r'''
\end{document}

''')
