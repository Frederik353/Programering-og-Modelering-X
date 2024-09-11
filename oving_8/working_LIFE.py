import sys
from time import time

import matplotlib.pyplot as plt
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
import pycuda.gpuarray as gpuarray
import pycuda.tools
from pycuda.compiler import SourceModule
from pylab import cm as cm

# n = 2**14  # 16k
n = 2**11  # 4k
# n = 2**8
# n_iter = 100_00
n_iter = 0
# n_iter=int(sys.argv[2])
n_block = 16
n_grid = int(n / n_block)
n = n_block * n_grid

import numpy as np


def random_init(n):
    M = np.random.randint(2, size=(n, n), dtype=np.int32)
    return M


# def random_init(n):
#     # np.random.seed(100)
#     M = np.zeros((n, n)).astype(np.int32)
#     for i in range(n):
#         print(i)
#         for j in range(n):
#             M[j, i] = np.int32(np.random.randint(2))
#     return M

with open("./LIFE/kernel2d.cu", 'r') as f:
    kernel = f.read()

mod = SourceModule(kernel)

func = mod.get_function("step")
C = random_init(n)
M = np.empty_like(C)
C_gpu = gpuarray.to_gpu(C)
M_gpu = gpuarray.to_gpu(M)
for k in range(n_iter):
    func(C_gpu, M_gpu, block=(n_block, n_block, 1), grid=(n_grid, n_grid, 1))
    C_gpu, M_gpu = M_gpu, C_gpu
print("%d live cells after %d iterations" % (np.sum(C_gpu.get()), n_iter))

fig = plt.figure(figsize=(29, 18))
ax = fig.add_subplot(111)
fig.suptitle("Conway's Game of Life Accelerated with PyCUDA")
ax.set_title('Number of Iterations = %d' % (n_iter))
myobj = plt.imshow(C_gpu.get(),
                   origin='lower',
                   cmap='Greys',
                   interpolation='nearest',
                   vmin=0,
                   vmax=1)
plt.pause(.01)
plt.draw()
m = n_iter
while True:
    m += 1
    t1 = time()
    func(C_gpu, M_gpu, block=(n_block, n_block, 1), grid=(n_grid, n_grid, 1))
    C_gpu, M_gpu = M_gpu, C_gpu
    myobj.set_data(C_gpu.get())
    t2 = time()
    print(t2 - t1)
    ax.set_title('Number of Iterations = %d' % (m))
    plt.pause(.00001)
    plt.draw()
