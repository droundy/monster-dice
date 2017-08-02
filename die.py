import matplotlib
matplotlib.use('Agg')

import glob, os, sys, string, numpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

light_colors = ['y', 'yellow', 'white']

imsz = 1.25
safesz = 1.0
lw = .25

bestcolor = {
    'black': '#000000',
    'yellow': "#ffe600",
    'orange': "#ff6600",
    'red': '#ff0000',
    'white': '#ffffff',
    'green': '#00b300',
    'blue': '#0000ff',
    'purple': '#800080',
}

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

def plotshield(sz,x0,y0,color):
    sz *= .8 # shrink a bit vs original design
    x = np.linspace(x0-sz/2,x0+sz/2,100)
    X = 2*(x-x0)/sz
    yshield = y0 + sz*(.5 - .6*(np.sqrt(abs(1-X**8))) + 0.5*(abs(X)-1))
    plt.fill_between(x,yshield,y0+sz/2, facecolor=bestcolor[color])

def plotheal(sz,x,y,color):
    plt.fill_between([x+sz/2, x-sz/2], [y-sz/6]*2, [y+sz/6]*2,facecolor=bestcolor[color])
    plt.fill_between([x+sz/6, x-sz/6], [y-sz/2]*2, [y+sz/2]*2,facecolor=bestcolor[color])

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
    plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', color=bestcolor[color], lw=4*sz)
    theta = np.linspace(0.7*2*np.pi, 0.8*2*np.pi, 50)
    r = sz/3*(1 + (theta/theta.max()-1)*3)
    plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', color=bestcolor[color], lw=4*sz)
    theta = np.linspace(0.71*2*np.pi, 0.8*2*np.pi, 50)
    r = sz/3*(1 - (theta/theta.max()-1)*3)
    plt.plot(x+r*np.cos(theta), y+r*np.sin(theta), '-', color=bestcolor[color], lw=4*sz)

def plotplus(sz, x, y, color, lw):
    plt.plot([x+sz/2, x-sz/2], [y,y], '-', lw=lw, color=bestcolor[color])
    plt.plot([x, x], [y+sz/2,y-sz/2], '-', lw=lw, color=bestcolor[color])
    r = np.linspace(0.7*sz/2, sz/2, 2)
    for theta in np.arange(0, 2*np.pi, np.pi/2):
        plt.plot(x+r*np.cos(np.linspace(theta-.2, theta,2)),
                 y+r*np.sin(np.linspace(theta-.2, theta,2)),
                 '-', lw=lw, color=bestcolor[color])
        plt.plot(x+r*np.cos(np.linspace(theta+.2, theta,2)),
                 y+r*np.sin(np.linspace(theta+.2, theta,2)),
                 '-', lw=lw, color=bestcolor[color])

def plotspecial(sz, x, y, color, lw):
    theta = np.linspace(0,  2*np.pi, 4)
    r = np.zeros_like(theta) + sz/2
    plt.plot(x+r*np.sin(theta), y+r*np.cos(theta), '-', color=bestcolor[color], lw=lw)

def gridtwo(sz, x0, y0, color, lw):
    # sz *= .9 # leave a bit of space...
    # for off in [-.1, -.3, .1, .3]:
    #     plt.plot([x+sz/2, x-sz/2], [y+sz*off,y+sz*off], '-', lw=lw, color=color)
    #     plt.plot([x+sz*off, x+sz*off], [y+sz/2,y-sz/2], '-', lw=lw, color=color)
    # for off in [-.5,.5]:
    #     plt.plot([x+sz*.3, x-sz*.3], [y+sz*off,y+sz*off], '-', lw=lw, color=color)
    #     plt.plot([x+sz*off, x+sz*off], [y+sz*.3,y-sz*.3], '-', lw=lw, color=color)
    R = sz*.9/2
    Rmin = sz*.8/2
    x = np.linspace(-R,R,200)
    dx = x[1]-x[0]
    ytop = np.sqrt(abs(R**2 - x**2))
    ybot = np.sqrt(abs(Rmin**2 - x**2))
    ybot[abs(x)>Rmin] = 0
    plt.fill_between(x0+x,y0+ybot,y0+ytop, facecolor=bestcolor[color])
    plt.fill_between(x0+x,y0-ybot,y0-ytop, facecolor=bestcolor[color])

def plotx(sz, x, y, color, lw):
    rad = sz/2
    sz /= np.sqrt(2)
    plt.plot([x+sz/2, x-sz/2], [y+sz/2,y-sz/2], '-', lw=lw, color=bestcolor[color])
    plt.plot([x+sz/2, x-sz/2], [y-sz/2,y+sz/2], '-', lw=lw, color=bestcolor[color])
    r = np.linspace(0.7*rad, rad, 2)
    for theta in np.arange(np.pi/4, 2*np.pi, np.pi/2):
        plt.plot(x+r*np.cos(np.linspace(theta-.2, theta,2)),
                 y+r*np.sin(np.linspace(theta-.2, theta,2)),
                 '-', lw=lw, color=bestcolor[color])
        plt.plot(x+r*np.cos(np.linspace(theta+.2, theta,2)),
                 y+r*np.sin(np.linspace(theta+.2, theta,2)),
                 '-', lw=lw, color=bestcolor[color])

def plotpow(sz, x, y, color='white'):
    X,Y = np.meshgrid(np.linspace(-sz/2,sz/2,100), np.linspace(-sz/2,sz/2,100))
    phi = np.arctan2(Y,X);
    r = np.sqrt(X**2+Y**2)
    dangle = np.pi/3.5
    relr = r/sz*2
    power = 8
    constant = 4
    pointiness = (constant+dangle)**power/(constant + phi % dangle)**power
    back = phi % dangle < dangle/2
    pointiness[back] = (constant+dangle)**power/(constant + (-phi[back]) % dangle)**power
    val = r*2/sz*pointiness;
    val[val>1] = np.nan
    if color in ['red', 'orange']:
        plt.contourf(x+X,y+Y,val,cmap='autumn')
    else:
        plt.contourf(x+X,y+Y,val,cmap='autumn_r')

def plotstatue(sz, x, y, color='black'):
    theta = np.linspace(0, 2*np.pi, 121)
    r = np.zeros_like(theta) + sz/2
    lw = 3*sz
    plt.plot(x+.3*r*np.cos(theta), y+.7*r+.3*r*np.sin(theta),
             '-', lw=lw, color=bestcolor[color])
    r = sz/2
    plt.plot([x,x,x+r/3], [y+.4*r, y-.2*r, y-.9*r], '-', lw=lw, color=bestcolor[color])
    plt.plot([x,x-r/3], [y-.2*r, y-.9*r], '-', lw=lw, color=bestcolor[color])
    plt.plot([x-r/3,x+r/3], [y+0.2*r, y+0.2*r], '-', lw=lw, color=bestcolor[color])

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
    if tok in 'RoFW32H':
        gridtwo(rad,x,y, color, 1)

    if tok == 'P':
        plotpow(rad,x,y, backcolor)
    elif tok == '+':
        plotplus(rad,x,y, color, 2)
    elif tok == '#':
        plotplus(rad,x,y, color, 2)
        plotpow(0.6*rad,x,y, backcolor)
    elif tok == 'x':
        plotx(rad,x,y, color, 2)
    elif tok == 'X':
        plotx(rad,x,y, color, 2)
        plotpow(0.6*rad,x,y, backcolor)
    elif tok == '*':
        plotx(rad,x,y, color, 2)
        plotplus(rad,x,y, color, 2)
    elif tok == '@':
        plotx(rad,x,y, color, 2)
        plotplus(rad,x,y, color, 2)
        plotpow(0.6*rad,x,y, backcolor)
    elif tok == 'b':
        plotspecial(rad,x,y, color, 2)
        plotstatue(0.6*rad,x,y,'black')
    elif tok == '2':
        plotpow(0.7*rad,x,y, backcolor)
    elif tok == '3':
        plotpow(0.7*rad,x,y, backcolor)
    elif tok == 'W':
        plotwing(.9*rad, x, y, (.8,.8,.6))
    elif tok == 'R':
        plotpow(0.7*rad,x,y, backcolor)
    elif tok == 'r':
        plotpow(rad,x,y, backcolor)
        plotretaliate(0.8*rad,x,y, color)
    elif tok == 'H':
        plotheal(0.55*rad,x,y, 'red')
    elif tok == 'A':
        plotshield(rad,x,y, color)
    elif tok == 'S':
        plotspecial(rad,x,y, color, 2)
    elif tok == 'B':
        plotspecial(rad,x,y, color, 2)
        plotpow(.5*rad,x+.25*rad,y, backcolor)
        plotpow(.5*rad,x-.25*rad,y, backcolor)
        plotpow(.5*rad,x,y+.25*rad, backcolor)
        plotpow(.5*rad,x,y-.25*rad, backcolor)
        plotpow(.5*rad,x,y, 'red')
    elif tok == 'f':
        plotspecial(rad,x,y, color, 2)
        plotwing(.9*rad, x, y, (.8,.8,.6))

def positions(side):
    sz = 1.8
    f = 0.95
    if side == 0:
        return []
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
    plt.gca().set_facecolor(bestcolor[m['color']])
    for i in range(side):
        x,y,rad = positions(side)[i]
        symbol(m['move'][i],rad,x,y,m['color'])
    for w in np.arange(0.03, .9, 0.03):
        text = plt.text(0, 0, name, color=directioncolor,
                        ha='center', va='center', size=14)
        text.set_path_effects([path_effects.Stroke(linewidth=1/w, alpha=w,
                                                   foreground=bestcolor[m['color']]),
                           path_effects.Normal()])


os.system('mkdir -p sides')
os.system('mkdir -p upload')
os.system('mkdir -p dice_app/images')

if sys.argv[1] == 'colortest':
    (c,v) = eval(sys.argv[2])
    colortest(c,v)
elif sys.argv[1] == 'monster':
    monster = eval(sys.argv[2])
    for side in [1,2,3,4,5,6]:
        plotme(monster, side)
        plt.savefig('sides/{}-{}.pdf'.format(monster['name'],side))
        plt.savefig('sides/{}-{}.png'.format(monster['name'],side), dpi=94)
        plt.savefig('upload/{}-{}[2].png'.format(monster['name'],side), dpi=94)
    imsz = 1.0
    for side in [1,2,3,4,5,6]:
        plt.cla()
        plotme(monster, side)
        plt.savefig('dice_app/images/{}-{}.png'.format(monster['name'],side), dpi=300)
elif sys.argv[1] == 'action':
    action = eval(sys.argv[2])
    for side in range(1,7):
        plt.close('all')
        plt.figure(figsize=(2,2))
        plt.xlim(-imsz,imsz)
        plt.ylim(-imsz,imsz)
        plt.gca().set_position([0, 0, 1, 1])
        plt.gca().set_facecolor(bestcolor[action['color']])
        for x,y,rad in positions(side):
            symbol(action['sides'][side-1],rad,x,y,action['color'])
        plt.savefig('sides/{}-{}.png'.format(action['color'],side), dpi=94)
        plt.savefig('upload/{}-{}[{}].png'.format(action['color'],side,action['count']),
                    dpi=94)
    for side in range(0,7):
        imsz = 1.0
        plt.clf()
        plt.xlim(-imsz,imsz)
        plt.ylim(-imsz,imsz)
        plt.gca().set_position([0, 0, 1, 1])
        plt.gca().set_facecolor(bestcolor[action['color']])
        for x,y,rad in positions(side):
            symbol(action['sides'][side-1],rad,x,y,action['color'])
        plt.savefig('dice_app/images/{}-{}.png'.format(action['color'],side), dpi=300)
elif sys.argv[1] == 'action-help':
    action = eval(sys.argv[2])
    imsz = 1.0
    plt.figure(figsize=(2,2))
    plt.xlim(-imsz,imsz)
    plt.ylim(-imsz,imsz)
    plt.gca().set_position([0, 0, 1, 1])
    plt.gca().set_facecolor(bestcolor[action['color']])
    symbol(action['move'],1.6,0,0,action['color'])
    plt.savefig('sides/{}.png'.format(action['name']), dpi=300)
