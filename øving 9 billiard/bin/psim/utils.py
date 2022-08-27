import cmath
import numpy as np

from numba import njit
from scipy.spatial.transform import Rotation

def normalize_rotation_vector(v):
    return Rotation.from_rotvec(v).as_rotvec()

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle(v2, v1=(1, 0)):
    ang = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
    if ang < 0:
        return 2*np.pi + ang

    return ang


def coordinate_rotation(v, phi):
    rotation = np.array([[np.cos(phi), -np.sin(phi), 0],
                         [np.sin(phi),  np.cos(phi), 0],
                         [0,  0, 1]])

    return np.matmul(rotation, v)
