import matplotlib
matplotlib.use('Agg')

import glob, os, string, numpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

os.system('mkdir -p sides')
os.system('mkdir -p upload')

light_colors = ['y', 'yellow', 'white']

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
     'move': '*ARWAf',
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
     'color': 'orange',
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
     'move': '+R*FB*',
     'color': 'purple',
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
     'color': 'white',
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
    { 'color': 'black',
      'sides': '**PX#@', },

    { 'color': 'blue',
      'sides': 'P+##+#', },
    { 'color': 'blue',
      'sides': 'P+##+#', },

    { 'color': 'green',
      'sides': 'XPXxxX', },
    { 'color': 'green',
      'sides': 'XPXxxX', },

    { 'color': 'yellow',
      'sides': '+#+2P3', },
    { 'color': 'yellow',
      'sides': '+#+2P3', },

    { 'color': 'orange',
      'sides': 'xxFPXF', },
    { 'color': 'white',
      'sides': 'xxFPXF', },

    { 'color': 'red',
      'sides': '2@*FPS', },
    { 'color': 'purple',
      'sides': '2@*FPS', },
]

imsz = 1.25
safesz = 1.0
lw = .25

def colortest(name, colors):
    plt.close('all')
    plt.figure(figsize=(2,2))
    plt.xlim(-imsz,imsz)
    plt.ylim(-imsz,imsz)
    plt.gca().set_position([0, 0, 1, 1])
    plt.gca().set_facecolor('white')
    farleft = np.linspace(-1,-.5,2)*imsz
    left = np.linspace(-.5,0,2)*imsz
    farright = np.linspace(1,.5,2)*imsz
    right = np.linspace(.5,0,2)*imsz
    top = [imsz,imsz]
    middle = [0,0]
    bottom = [-imsz,-imsz]
    plt.fill_between(farleft,middle,top, facecolor=colors[0])
    plt.fill_between(left,middle,top, facecolor=colors[1])
    plt.fill_between(right,middle,top, facecolor=colors[2])
    plt.fill_between(farright,middle,top, facecolor=colors[3])
    plt.fill_between(farleft,middle,bottom, facecolor=colors[4])
    plt.fill_between(left,middle,bottom, facecolor=colors[5])
    plt.fill_between(right,middle,bottom, facecolor=colors[6])
    plt.fill_between(farright,middle,bottom, facecolor=colors[7])
    text = plt.text(0, 0, name, color='white',
                    ha='center', va='center', size=24)
    plt.savefig('upload/test-{}.png'.format(name), dpi=94)

colortest('greens', [(0,1,0), (0,0.9,0), (0,0.8,0), (0,0.6,0),
                     (0,.95,0), (0,0.85,0), (0,0.7,0), (0,0.5,0),
])
colortest('yellows', [(1,1,0), 'yellow', (0.9,0.9,0), (0.8,0.8,0),
                     (.9,1,0), (1,0.9,0), (0.7,.7,0), (0.6,0.6,0),
])
colortest('purples', ['purple', (1,0,1), (0.9,0,1), (0.8,0,1),
                     (.7,0,1), (.6,0,1), (0.5,0,1), (0.4,0,1),
])
colortest('oranges', ['orange', (1,.5,0), (1,.6,0), (1,.7,0),
                     (1,.4,0), (1,.3,0), (1,0.2,0), (.8,.4,0),
])
colortest('blues', [(0,0,1), (0,0,0.9), (0,0,0.8), (0,0,0.7),
                     (0,0,.95), (0,0,0.85), (0,0,0.75), (0,0,0.65),
])
colortest('reds', [(1,0,0), (0.9,0,0), (0.8,0,0), (0.7,0,0),
                     (.95,0,0), (0.85,0,0), (0.75,0,0), (0.65,0,0),
])

def plotshield(sz,x0,y0,color):
    sz *= .8 # shrink a bit vs original design
    x = np.linspace(x0-sz/2,x0+sz/2,100)
    X = 2*(x-x0)/sz
    yshield = y0 + sz*(.5 - .6*(np.sqrt(abs(1-X**8))) + 0.5*(abs(X)-1))
    plt.fill_between(x,yshield,y0+sz/2, facecolor=color)

def plotheal(sz,x,y,color):
    plt.fill_between([x+sz/2, x-sz/2], [y-sz/6]*2, [y+sz/6]*2,facecolor=color)
    plt.fill_between([x+sz/6, x-sz/6], [y-sz/2]*2, [y+sz/2]*2,facecolor=color)

def plotheart(sz,x00,y00,color):
    R = sz*.275/.5
    x0 = .4*sz
    x = np.linspace(-R-x0,R+x0,200)
    dx = x[1]-x[0]
    ytop = np.zeros_like(x)
    ytop[x>=0] = np.sqrt(abs(R**2 - (x[x>=0]-x0)**2))
    ytop[x<=0] = np.sqrt(abs(R**2 - (x[x<=0]+x0)**2))
    ybot = -ytop.copy()
    i=95
    while i >= 0:
        if ybot[100+i] > ybot[100+i+1] - dx*.7:
            ybot[100+i] = 2*ybot[100+i+1] - ybot[100+i+2]
            ybot[100-i] = ybot[100+i]
        i-=1
    plt.fill_between(x00+x,y00+ybot,y00+ytop, facecolor=color)

def plotrange(sz,color):
    R = sz*.275/.5
    x0 = .5
    x = np.linspace(x0-R,R+x0,100)
    dx = x[1]-x[0]
    ytop =  np.sqrt(R**2 - (x-x0)**2) -.5
    ybot = -np.sqrt(R**2 - (x-x0)**2) -.5
    plt.fill_between(x,ybot,ytop, facecolor=color)

def plotwing(sz, x0, y0, color):
    x = np.linspace(-sz*.6,sz*.6,100)
    X = abs(x/max(x))
    wingtop = 0.5*(1 + 4*X - np.sqrt((4*X)**2 + 1))
    wingbot = wingtop - 0.3*(.2+X)*np.sqrt(1-X)
    yoff = 0.0*sz
    plt.fill_between(1.1*x+x0,
                     y0+wingtop*sz+yoff,
                     y0+wingbot*sz+yoff, facecolor=color)
    plt.fill_between(.9*x+x0,
                     y0+.8*wingtop*sz+yoff,
                     y0+.8*wingbot*sz+yoff, facecolor=color)
    wingbot = wingtop - 0.6*(.2+X)*np.sqrt(1-X)
    plt.fill_between(.8*x+x0,
                     y0+.6*wingtop*sz+yoff,
                     y0+.6*wingbot*sz+yoff, facecolor=color)
    plt.fill_between(.7*x+x0,
                     y0+.4*wingtop*sz+yoff,
                     y0+.4*wingbot*sz+yoff, facecolor=color)

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
    r = np.linspace(0.7*sz/2, sz/2, 2)
    for theta in np.arange(0, 2*np.pi, np.pi/2):
        plt.plot(x+r*np.cos(np.linspace(theta-.2, theta,2)),
                 y+r*np.sin(np.linspace(theta-.2, theta,2)), '-', lw=lw, color=color)
        plt.plot(x+r*np.cos(np.linspace(theta+.2, theta,2)),
                 y+r*np.sin(np.linspace(theta+.2, theta,2)), '-', lw=lw, color=color)

def plotspecial(sz, x, y, color, lw):
    theta = np.linspace(0,  2*np.pi, 4)
    r = np.zeros_like(theta) + sz/2
    plt.plot(x+r*np.sin(theta), y+r*np.cos(theta), '-', color=color, lw=lw)

def gridtwo(sz, x, y, color, lw):
    sz *= .9 # leave a bit of space...
    for off in [-.1, -.3, .1, .3]:
        plt.plot([x+sz/2, x-sz/2], [y+sz*off,y+sz*off], '-', lw=lw, color=color)
        plt.plot([x+sz*off, x+sz*off], [y+sz/2,y-sz/2], '-', lw=lw, color=color)
    for off in [-.5,.5]:
        plt.plot([x+sz*.3, x-sz*.3], [y+sz*off,y+sz*off], '-', lw=lw, color=color)
        plt.plot([x+sz*off, x+sz*off], [y+sz*.3,y-sz*.3], '-', lw=lw, color=color)

def plotx(sz, x, y, color, lw):
    rad = sz/2
    sz /= np.sqrt(2)
    plt.plot([x+sz/2, x-sz/2], [y+sz/2,y-sz/2], '-', lw=lw, color=color)
    plt.plot([x+sz/2, x-sz/2], [y-sz/2,y+sz/2], '-', lw=lw, color=color)
    r = np.linspace(0.7*rad, rad, 2)
    for theta in np.arange(np.pi/4, 2*np.pi, np.pi/2):
        plt.plot(x+r*np.cos(np.linspace(theta-.2, theta,2)),
                 y+r*np.sin(np.linspace(theta-.2, theta,2)), '-', lw=lw, color=color)
        plt.plot(x+r*np.cos(np.linspace(theta+.2, theta,2)),
                 y+r*np.sin(np.linspace(theta+.2, theta,2)), '-', lw=lw, color=color)

def plotpow(sz, x, y, color='w'):
    theta = np.linspace(0, 2*np.pi, 21)
    r = np.zeros_like(theta) + sz/2
    r[::2] /= 2;
    plt.plot(x+.3*r*np.cos(theta), y+.3*r*np.sin(theta), '-', lw=8*sz, color='white')
    plt.plot(x+.6*r*np.cos(theta), y+.6*r*np.sin(theta), '-', lw=2.5*sz, color='yellow')
    plt.plot(x+.8*r*np.cos(theta), y+.8*r*np.sin(theta), '-', lw=2.5*sz, color='orange')
    if color == 'red':
        plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', lw=2.5*sz, color='orange')
    else:
        plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', lw=2.5*sz, color='red')

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
    if backcolor in light_colors:
        color = 'black'
    if tok == 'P':
        plotpow(rad,x,y, backcolor)
    elif tok == '+':
        plotplus(rad,x,y, color, 2)
    elif tok == '#':
        plotplus(rad,x,y, color, 2)
        plotpow(0.6*rad,x,y)
    elif tok == 'x':
        plotx(rad,x,y, color, 2)
    elif tok == 'X':
        plotx(rad,x,y, color, 2)
        plotpow(0.6*rad,x,y)
    elif tok == '*':
        plotx(rad,x,y, color, 2)
        plotplus(rad,x,y, color, 2)
    elif tok == '@':
        plotx(rad,x,y, color, 2)
        plotplus(rad,x,y, color, 2)
        plotpow(0.6*rad,x,y)
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
        plotheal(0.3*rad,x,y, 'red')
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
    sz = 1.8
    f = 0.95
    if side == 1:
        return [(0,0,f*sz)]
    if side == 2:
        return [(-sz/4,-sz/4,sz/2), (sz/4,sz/4,sz/2)]
    if side == 3:
        return [(-sz/4,-sz/4,f*sz/2), (sz/4,-sz/4,f*sz/2), (0,sz/4,f*sz/2)]
    if side == 4:
        return [(-sz/4,sz/4,f**2*sz/2), (-sz/4,-sz/4,f**2*sz/2),
                (sz/4,-sz/4,f**2*sz/2), (sz/4,sz/4,f**2*sz/2)]
    if side == 5:
        p = []
        z = 0.6
        r = sz/2 - z/2
        for i in reversed(range(5)):
            p.append((r*np.sin(i*2*np.pi/5), r*np.cos(i*2*np.pi/5), z))
        return p
        # return [(x,-x,1/np.sqrt(2)), (-x,-x,1/np.sqrt(2)),
        #         (x,x,1/np.sqrt(2)), (-x,x,1/np.sqrt(2)), (0,0,1/np.sqrt(2))]
    if side == 6:
        f = 1 # np.sqrt(f)
        return [(-sz/3, sz/5, f*sz/3),
                (-sz/3,-sz/5, f*sz/3),
                 (    0,-sz/3, f*sz/3),
                ( sz/3,-sz/5, f*sz/3),
                ( sz/3, sz/5, f*sz/3),
                (    0, sz/3, f*sz/3),
        ]
        return [( sz/3,-sz/3, f*sz/3),
                (    0,-sz/3, f*sz/3),
                (-sz/3,- sz/3, f*sz/3),
                (sz/3,-sz/3, f*sz/3),
                (sz/3,    0, f*sz/3),
                (sz/3, sz/3, f*sz/3),
        ]
        z = 0.5
        r = sz/2 - z/2
        p = [(0,0,(sz-2*z))]
        for i in reversed(range(5)):
            p.append((r*np.sin(i*2*np.pi/5), r*np.cos(i*2*np.pi/5), z))
        return p

def proper_color(color):
    if color == 'orange':
        return (1, 0.4, 0)
    return color

def plotme(m, side):
    name = m['name']
    plt.close('all')
    plt.figure(figsize=(2,2))
    plt.xlim(-imsz,imsz)
    plt.ylim(-imsz,imsz)
    plt.gca().set_position([0, 0, 1, 1])
    directioncolor = 'white'
    if m['color'] in light_colors:
        directioncolor = 'black'
    plt.gca().set_facecolor(proper_color(m['color']))
    for i in range(side):
        x,y,rad = positions(side)[i]
        symbol(m['move'][i],rad,x,y,m['color'])
    for w in np.arange(0.03, .9, 0.03):
        text = plt.text(0, 0, name, color=directioncolor,
                        ha='center', va='center', size=14)
        text.set_path_effects([path_effects.Stroke(linewidth=1/w, alpha=w,
                                                   foreground=proper_color(m['color'])),
                           path_effects.Normal()])
for monster in monsters:
    for side in [1,2,3,4,5,6]:
        # fac.write('| xelatex {}-{}\n\n'.format(monster,side))
        plotme(monster, side)
        plt.savefig('sides/{}-{}.pdf'.format(monster['name'],side))
        plt.savefig('sides/{}-{}.png'.format(monster['name'],side), dpi=94)
        plt.savefig('upload/{}-{}[2].png'.format(monster['name'],side), dpi=94)

already_done = set({})
for action in actions:
    for side in range(1,7):
        plt.close('all')
        plt.figure(figsize=(2,2))
        plt.xlim(-imsz,imsz)
        plt.ylim(-imsz,imsz)
        plt.gca().set_position([0, 0, 1, 1])
        plt.gca().set_facecolor(proper_color(action['color']))
        for x,y,rad in positions(side):
            symbol(action['sides'][side-1],rad,x,y,action['color'])
        plt.savefig('sides/{}-{}.png'.format(action['color'],side), dpi=94)
        if action['color'] in already_done:
            plt.savefig('upload/{}-{}[2].png'.format(action['color'],side), dpi=94)
        else:
            plt.savefig('upload/{}-{}[1].png'.format(action['color'],side), dpi=94)
    already_done.add(action['color'])

with open('paper.tex'.format(monster,side),'w') as f:
    f.write(r'''\documentclass[11pt]{article}

\usepackage{graphicx}
\usepackage{lmodern}
\usepackage{fullpage}

\begin{document}
\noindent
''')
    i = 0
    for monster in monsters:
        if not (i & 1):
            f.write(r'\hspace{-0.5in}')
        for side in [1,2,3,4,5,6]:
            f.write(r'\includegraphics[width=0.625in]{{sides/{}-{}}}'
                    .format(monster['name'],side))
        if i & 1:
            f.write('\\\\\n\\vspace{-2pt}')
        i += 1
    for action in actions:
        if not (i & 1):
            f.write(r'\hspace{-0.5in}')
        for side in [1,2,3,4,5,6]:
            f.write(r'\includegraphics[width=0.625in]{{sides/{}-{}}}'
                    .format(action['color'],side))
        if i & 1:
            f.write('\\\\\n\\vspace{-2pt}')
        i += 1
    f.write(r'''
\end{document}

''')
