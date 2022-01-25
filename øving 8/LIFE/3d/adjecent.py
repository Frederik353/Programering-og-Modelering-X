import numpy as np

def get_neighbours(p, exclude_p=True, shape=None):

    ndim = len(p)

    # generate an (m, ndims) array containing all strings over the alphabet {0, 1, 2}:
    print(np.indices((3,) * ndim))
    offset_idx = np.indices((3,) * ndim).reshape(ndim, -1).T

    # use these to index into np.array([-1, 0, 1]) to get offsets
    offsets = np.r_[-1, 0, 1].take(offset_idx)
    # print(offsets)

    # optional: exclude offsets of 0, 0, ..., 0 (i.e. p itself)
    if exclude_p:
        offsets = offsets[np.any(offsets, 1)]

    neighbours = p + offsets # apply offsets to p

    # wrap
    if shape is not None:
        neighbours = np.where(neighbours > np.array(shape) - 1, 0 , neighbours) # upper bound
        neighbours = np.where(neighbours < 0, np.array(shape) - 1 , neighbours) # lower bound

    return neighbours



p = np.r_[0, 0]
shape = (6, 6)

neighbours = get_neighbours(p, shape=shape)
# print(neighbours)
x = np.zeros(shape, int)
x[tuple(neighbours.T)] = 1
x[tuple(p)] = 2

print(x)