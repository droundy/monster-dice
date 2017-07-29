import matplotlib
matplotlib.use('Agg')

import glob, os, sys, string, numpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

blank = {
    'move': 'xxxxxx',
    'color': 'brown',
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
    },
    {**blank,
     'name': 'spearman',
     'move': '+r++++',
     'color': 'blue',
    },
    {**blank,
     'name': 'axeman',
     'move': 'xxxxxx',
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
      'sides': '**PX#@',
      'count': 2, },

    { 'color': 'blue',
      'sides': 'P+##+#',
      'count': 2, },

    { 'color': 'green',
      'sides': 'XPXxxX',
      'count': 2, },

    { 'color': 'yellow',
      'sides': '+#+2P3',
      'count': 2, },

    { 'color': 'orange',
      'sides': 'xxFPXF',
      'count': 1, },
    { 'color': 'white',
      'sides': 'xxFPXF',
      'count': 1, },

    { 'color': 'red',
      'sides': '2@*FPS',
      'count': 1, },
    { 'color': 'purple',
      'sides': '2@*FPS',
      'count': 1, },
]

colortests = {
    'greens': [(0,1,0), (0,0.9,0), (0,0.8,0), (0,0.6,0),
               (0,.95,0), (0,0.85,0), (0,0.7,0), (0,0.5,0)],
    'yellows': [(1,1,0), 'yellow', (0.9,0.9,0), (0.8,0.8,0),
                (.9,1,0), (1,0.9,0), (0.7,.7,0), (0.6,0.6,0)],
    'purples': ['purple', (1,0,1), (0.9,0,1), (0.8,0,1),
                (.7,0,1), (.6,0,1), (0.5,0,1), (0.4,0,1)],
    'oranges': ['orange', (1,.5,0), (1,.6,0), (1,.7,0),
                (1,.4,0), (1,.3,0), (1,0.2,0), (.8,.4,0)],
    'blues': [(0,0,1), (0,0,0.9), (0,0,0.8), (0,0,0.7),
              (0,0,.95), (0,0,0.85), (0,0,0.75), (0,0,0.65)],
    'reds': [(1,0,0), (0.9,0,0), (0.8,0,0), (0.7,0,0),
             (.95,0,0), (0.85,0,0), (0.75,0,0), (0.65,0,0)],
}
