import numpy as np

from scipy.spatial.transform import Rotation

def normalize_rotation_vector(v):
    # gir den minste representasjonen av rotasjons vektoren
    return Rotation.from_rotvec(v).as_rotvec()

def unit_vector(vector):
    # returnerer en normalisert vektor alstså en enhetsvektor
    return vector / np.linalg.norm(vector)

def angle(v2, v1=(1, 0)):
    # gir vinkelen mellom to vektorer i radianer
    ang = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
    if ang < 0:
        return 2*np.pi + ang

    return ang


def coordinate_rotation(v, phi):
    # roterer et koordinat rundt origo
    rotation = np.array([[np.cos(phi), -np.sin(phi), 0],
                         [np.sin(phi),  np.cos(phi), 0],
                         [0,  0, 1]])

    return np.matmul(rotation, v)
