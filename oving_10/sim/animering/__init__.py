

SPOR_LENGDE = 200

# pixler i den største dimensjonen
MAX_SCREEN = 700

BORD_MERKE_FARGE = (0,0,0)
BORD_KANT_FARGE = (112, 79, 50)
VEGG_STOFF_FARGE = (30,54,40)
STOFF_FARGE = (44,130,87)
VEGG_FARGE = (71,38,27)
KULE_FARGER = {
    'stav': (244,242,238),
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
    if hasattr(d, '__len__'):
        return (d * scale + offset).astype(int)
    else:
        return int(d * scale + offset)


def px_to_d(scale):
    return d / scale

