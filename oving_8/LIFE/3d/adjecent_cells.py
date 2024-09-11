import numpy as np

def get_neighbours(ndim, exclude_p=True):


    # print(np.indices((3,) * ndim))
    offset_idx = np.indices((3,) * ndim).reshape(ndim, -1).T

    offsets = np.r_[-1, 0, 1].take(offset_idx)
    print(offsets)

    # optional: exclude offsets of 0, 0, ..., 0 (i.e. p itself)
    if exclude_p:
        offsets = offsets[np.any(offsets, 1)]

    return offsets



# ndim = 4
# offsets = get_neighbours(ndim)



