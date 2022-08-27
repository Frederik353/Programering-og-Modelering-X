import psim

import os
import numpy as np

from pathlib import Path
from panda3d.core import *

loadPrcFile(str(Path(psim.__file__).parent / 'Config.prc'))

model_paths = (path for path in (Path(psim.__file__).parent.parent / 'models').glob('*') if path.is_file())
model_paths = {str(path.stem): Filename.fromOsSpecific(str(path.absolute())) for path in model_paths}

fps_target = 60

ghost_trail_array = np.arange(0,20,2)
line_trail_array = np.arange(1, 100, 1)
line_trail_thickness = 2
line_trail_color = LColor(1, 1, 1, 1)
ghost_decay = 4
line_decay = 3

TRACE_LENGTH = 50

# num of pixels of largest dimension
MAX_SCREEN = 700

DIAMOND_COLOR = (0,0,0)
EDGE_COLOR = (112, 79, 50)
RAIL_CLOTH_COLOR = (30,54,40)
CLOTH_COLOR = (44,130,87)
RAIL_COLOR = (71,38,27)
BALL_COLORS = {
    'cue': (244,242,238),
    '1': (0,0,139),
    '2': (4,93,184),
    '3': (255,0,0),
    '4': (160,32,240),
    '5': (255,140,0),
    '6': (0,255,0),
    '7': (128,0,32),
    '8': (0,0,0),
    '9': (0,0,139),
    '10': (4,93,184),
    '11': (255,0,0),
    '12': (160,32,240),
    '13': (255,140,0),
    '14': (0,255,0),
    '15': (128,0,32),
}

def d_to_px(scale, d, offset=0):
    """scale is ratio of d to px"""
    if hasattr(d, '__len__'):
        return (d * scale + offset).astype(int)
    else:
        return int(d * scale + offset)


def px_to_d(scale, px):
    """scale is ratio of d to px"""
    return d / scale

