import numpy as np

# n = 2 ** 12
n = 2 ** 5

ndim = 3


shape = (ndim,n)
C = np.random.randint(0,2, shape)

M = np.empty_like(C)

np.save('./bin/C', C)
np.save('./bin/M', M)





# def random_init(n):
#     # np.random.seed(100)
#     M = np.zeros((n, n, n)).astype(np.int32)
#     for i in range(n):
#         for j in range(n):
#             for k in range(n):
#                 M[k, j, i] = np.int32(np.random.randint(2))
#     return M

