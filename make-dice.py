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
    'range': [0]*6,
    'retaliate': [0]*6,
}

monsters = [
    {**blank,
     'name': 'orc',
     'move': 'xx****',
     'color': 'black',
    },
    {**blank,
     'name': 'dragon',
     'move': '+A*RWf',
     'color': 'red',
    },
    {**blank,
     'name': 'troll',
     'move': '++A+++',
     'color': 'blue',
    },
    {**blank,
     'name': 'ogre',
     'move': 'xxAxxx',
     'color': 'green',
    },
    {**blank,
     'name': 'griffin',
     'move': 'xxFxxx',
     'color': 'brown',
    },
    {**blank,
     'name': 'basilisk',
     'move': '+R+++*',
     'color': 'yellow',
    },
    {**blank,
     'name': 'swordsman',
     'move': '+r*A**',
     'color': 'black',
    },
    {**blank,
     'name': 'mage',
     'move': '+R*F*B',
     'color': 'red',
     'range': [1,1,1,1,1,1],
    },
    {**blank,
     'name': 'spearman',
     'move': '+r++++',
     'color': 'blue',
    },
    {**blank,
     'name': 'axeman',
     'move': ['x']*6,
     'color': 'green',
    },
    {**blank,
     'name': 'healer',
     'move': 'xHxx**',
     'color': 'brown',
    },
    {**blank,
     'name': 'archer',
     'move': '+R+++*',
     'color': 'yellow',
    },
]

actions = [
    { 'color': 'black',
      'sides': '**PX#@', },
    { 'color': 'blue',
      'sides': 'P+##+#', },
    { 'color': 'green',
      'sides': 'XPXxxX', },
    { 'color': 'yellow',
      'sides': '+#+2P3', },
    { 'color': 'brown',
      'sides': 'xxFPXF', },
    { 'color': 'red',
      'sides': '2@*FPS', },
]

imsz = 1.25
safesz = 1.0
lw = .25

def plotshield(sz,x0,y0,color):
    x = np.linspace(x0-sz/2,x0+sz/2,100)
    X = 2*(x-x0)/sz
    yshield = y0 + sz*(.5 - .6*(np.sqrt(1-X**8)) + 0.5*(abs(X)-1))
    plt.fill_between(x,yshield,y0+sz/2, facecolor=color)

def plotheal(sz,x00,y00,color):
    R = sz*.275/.5
    x0 = .4*sz
    x = np.linspace(-R/1000,R+x0,100)
    dx = x[1]-x[0]
    ytop = np.sqrt(R**2 - (x-x0)**2) -.02*sz
    ybot = -np.sqrt(R**2 - (x-x0)**2) -.02*sz
    i=95
    while i >= 0:
        if ybot[i] > ybot[i+1] - dx*.7:
            ybot[i] = 2*ybot[i+1] - ybot[i+2]
        i-=1
    plt.fill_between(x00+x,y00+ybot,y00+ytop, facecolor=color)
    plt.fill_between(x00-x,y00+ybot,y00+ ytop, facecolor=color)

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
    wingtop = y0-.5*sz + 0.8*(1 + 4*X - np.sqrt((4*X)**2 + 1))
    wingbot = wingtop - 0.3*(.2+X)*np.sqrt(1-X)
    plt.fill_between(1.1*x+x0,wingtop*sz,wingbot*sz, facecolor=color)
    plt.fill_between(.9*x+x0,.8*wingtop*sz,.8*wingbot*sz, facecolor=color)
    plt.fill_between(.8*x+x0,.65*wingtop*sz,.65*wingbot*sz, facecolor=color)

def plotretaliate(sz,x,y,color):
    theta = np.linspace(0, 0.8*2*np.pi, 200)
    r = np.zeros_like(theta) + sz/3
    plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', color=color, lw=3*sz)
    theta = np.linspace(0.7*2*np.pi, 0.8*2*np.pi, 50)
    r = sz/3*(1 + (theta/theta.max()-1)*3)
    plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', color=color, lw=3*sz)
    theta = np.linspace(0.71*2*np.pi, 0.8*2*np.pi, 50)
    r = sz/3*(1 - (theta/theta.max()-1)*3)
    plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', color=color, lw=3*sz)

def plotplus(sz, x, y, color, lw):
    plt.plot([x+sz/2, x-sz/2], [y,y], '-', lw=lw, color=color)
    plt.plot([x, x], [y+sz/2,y-sz/2], '-', lw=lw, color=color)
    plt.plot([x+3*sz/8, x+sz/2], [y+sz/8,y], '-', lw=lw, color=color)
    plt.plot([x+3*sz/8, x+sz/2], [y-sz/8,y], '-', lw=lw, color=color)
    plt.plot([x-3*sz/8, x-sz/2], [y+sz/8,y], '-', lw=lw, color=color)
    plt.plot([x-3*sz/8, x-sz/2], [y-sz/8,y], '-', lw=lw, color=color)
    plt.plot([x+sz/8, x], [y+3*sz/8,y+sz/2], '-', lw=lw, color=color)
    plt.plot([x-sz/8, x], [y+3*sz/8,y+sz/2], '-', lw=lw, color=color)
    plt.plot([x+sz/8, x], [y-3*sz/8,y-sz/2], '-', lw=lw, color=color)
    plt.plot([x-sz/8, x], [y-3*sz/8,y-sz/2], '-', lw=lw, color=color)

def plotspecial(sz, x, y, color, lw):
    theta = np.linspace(0,  2*np.pi, 4)
    r = np.zeros_like(theta) + sz/2
    plt.plot(x+r*np.sin(theta), y+r*np.cos(theta), '-', color=color, lw=lw)

def gridtwo(sz, x, y, color, lw):
    for off in [-.1, -.3, .1, .3]:
        plt.plot([x+sz/2, x-sz/2], [y+sz*off,y+sz*off], '-', lw=lw, color=color)
        plt.plot([x+sz*off, x+sz*off], [y+sz/2,y-sz/2], '-', lw=lw, color=color)
    for off in [-.5,.5]:
        plt.plot([x+sz*.3, x-sz*.3], [y+sz*off,y+sz*off], '-', lw=lw, color=color)
        plt.plot([x+sz*off, x+sz*off], [y+sz*.3,y-sz*.3], '-', lw=lw, color=color)

def plotx(sz, x, y, color, lw):
    sz /= np.sqrt(2)
    plt.plot([x+sz/2, x-sz/2], [y+sz/2,y-sz/2], '-', lw=lw, color=color)
    plt.plot([x+sz/2, x-sz/2], [y-sz/2,y+sz/2], '-', lw=lw, color=color)

    plt.plot([x+sz/2, x+sz/2], [y-sz/2,y-sz/4], '-', lw=lw, color=color)
    plt.plot([x+sz/2, x+sz/2], [y+sz/2,y+sz/4], '-', lw=lw, color=color)
    plt.plot([x-sz/2, x-sz/2], [y-sz/2,y-sz/4], '-', lw=lw, color=color)
    plt.plot([x-sz/2, x-sz/2], [y+sz/2,y+sz/4], '-', lw=lw, color=color)

    plt.plot([x-sz/2, x-sz/4], [y+sz/2,y+sz/2], '-', lw=lw, color=color)
    plt.plot([x+sz/2, x+sz/4], [y+sz/2,y+sz/2], '-', lw=lw, color=color)
    plt.plot([x-sz/2, x-sz/4], [y-sz/2,y-sz/2], '-', lw=lw, color=color)
    plt.plot([x+sz/2, x+sz/4], [y-sz/2,y-sz/2], '-', lw=lw, color=color)

def plotpow(sz, x, y, color='w'):
    theta = np.linspace(0, 2*np.pi, 21)
    r = np.zeros_like(theta) + sz/2
    r[::2] /= 2;
    plt.plot(x+.3*r*np.cos(theta), y+.3*r*np.sin(theta), '-', lw=8*sz, color='white')
    plt.plot(x+.6*r*np.cos(theta), y+.6*r*np.sin(theta), '-', lw=2*sz, color='yellow')
    plt.plot(x+.8*r*np.cos(theta), y+.8*r*np.sin(theta), '-', lw=2*sz, color='orange')
    if color == 'red':
        plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', lw=2*sz, color='orange')
    else:
        plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', lw=2*sz, color='red')

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

def symbol(tok, rad, x, y, backcolor):
    color = 'white'
    if backcolor in ['y', 'yellow']:
        color = 'black'
    if tok == 'P':
        plotpow(rad,x,y, backcolor)
    elif tok == '+':
        plotplus(rad,x,y, color, 2)
    elif tok == '#':
        plotplus(rad,x,y, color, 2)
        plotpow(0.3,x,y)
    elif tok == 'x':
        plotx(rad,x,y, color, 2)
    elif tok == 'X':
        plotx(rad,x,y, color, 2)
        plotpow(0.3,x,y)
    elif tok == '*':
        plotx(rad,x,y, color, 2)
        plotplus(rad,x,y, color, 2)
    elif tok == '@':
        plotx(rad,x,y, color, 2)
        plotplus(rad,x,y, color, 2)
        plotpow(0.3,x,y)
    elif tok == '2':
        gridtwo(rad,x,y, color, 1)
        plotpow(0.7*rad,x,y)
    elif tok == '3':
        gridtwo(rad,x,y, color, 1)
        plotpow(0.7*rad,x,y)
    elif tok == 'F':
        gridtwo(rad,x,y, color, 1)
    elif tok == 'W':
        gridtwo(rad,x,y, color, 1)
        plotwing(.9*rad, x, y, (.8,.8,.6))
    elif tok == 'R':
        gridtwo(rad,x,y, color, 1)
        plotpow(0.7*rad,x,y)
    elif tok == 'r':
        plotpow(0.8*rad, x, y)
        plotretaliate(rad,x,y, color)
    elif tok == 'H':
        gridtwo(rad,x,y, color, 1)
        plotheal(0.4*rad,x,y, color)
    elif tok == 'A':
        plotshield(rad,x,y, color)
    elif tok == 'S':
        plotspecial(rad,x,y, color, 2)
    elif tok == 'B':
        plotspecial(rad,x,y, color, 2)
        plotpow(.5*rad,x+.25*rad,y, color)
        plotpow(.5*rad,x-.25*rad,y, color)
        plotpow(.5*rad,x,y+.25*rad, color)
        plotpow(.5*rad,x,y-.25*rad, color)
        plotpow(.5*rad,x,y, 'black')
    elif tok == 'f':
        plotspecial(rad,x,y, color, 2)
        plotwing(.9*rad, x, y, (.8,.8,.6))
    else:
        plotpow(rad,x,y)

def positions(side):
    x = .55
    if side == 1:
        return [(0,0)]
    if side == 2:
        return [(x,x), (-x,-x)]
    if side == 3:
        return [(x,-x), (-x,-x), (0,x)]
    if side == 4:
        return [(x,-x), (-x,-x), (x,x), (-x,x)]
    if side == 5:
        return [(x,-x), (-x,-x), (x,x), (-x,x), (0,0)]
    if side == 6:
        return [(x,-x), (-x,-x), (x,x), (-x,x), (x,0), (-x,0)]

def plotme(m, side):
    name = m['name']
    plt.figure(figsize=(2,2))
    plt.xlim(-imsz,imsz)
    plt.ylim(-imsz,imsz)
    plt.gca().set_position([0, 0, 1, 1])
    directioncolor = 'white'
    if m['color'] in ['y', 'yellow']:
        directioncolor = 'black'
    plt.gca().set_facecolor(m['color'])
    rad = 1.0
    for i in range(side):
        x,y = positions(side)[i]
        symbol(m['move'][i],rad - (rad-.48)*side/6,x,y,m['color'])
    y = 0
    if side in [1,5]:
        y = -.6
    for w in np.arange(0.03, .9, 0.03):
        text = plt.text(0, y, name, color=directioncolor,
                        ha='center', va='center', size=14)
        text.set_path_effects([path_effects.Stroke(linewidth=1/w, alpha=w, foreground=m['color']),
                           path_effects.Normal()])
for monster in monsters:
    for side in [1,2,3,4,5,6]:
        # fac.write('| xelatex {}-{}\n\n'.format(monster,side))
        plotme(monster, side)
        plt.savefig('sides/{}-{}.pdf'.format(monster['name'],side))
        plt.savefig('sides/{}-{}.png'.format(monster['name'],side), dpi=94)

for action in actions:
    rad = 1.0
    for side in range(1,7):
        plt.figure(figsize=(2,2))
        plt.xlim(-imsz,imsz)
        plt.ylim(-imsz,imsz)
        plt.gca().set_position([0, 0, 1, 1])
        plt.gca().set_facecolor(action['color'])
        for (x,y) in positions(side):
            symbol(action['sides'][side-1],rad - (rad-.48)*side/6,x,y,action['color'])
        plt.savefig('sides/{}-{}.png'.format(action['color'],side), dpi=94)

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
        f.write('\\\\\n\\vspace{-2pt}')
    for action in actions:
        for side in [1,2,3,4,5,6]:
            f.write(r'\includegraphics[width=0.5in]{{sides/{}-{}}}'
                    .format(action['color'],side))
        f.write('\\\\\n\\vspace{-2pt}')
    f.write(r'''
\end{document}

''')
