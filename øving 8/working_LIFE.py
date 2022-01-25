import pycuda.driver as cuda
import pycuda.tools
import pycuda.autoinit
import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
import sys
import numpy as np
from pylab import cm as cm
import matplotlib.pyplot as plt
from time import time

# n = 2 ** 12  # 4k
n = 2 ** 10
n_iter = 100_00
# n_iter = 0  # n_iter=int(sys.argv[2])
n_block = 16
n_grid = int(n/n_block)
n = n_block*n_grid


def random_init(n):
    # np.random.seed(100)
    M = np.zeros((n, n)).astype(np.int32)
    for i in range(n):
        for j in range(n):
            M[j, i] = np.int32(np.random.randint(2))
    return M


with open("./øving 8 ferdig/LIFE/kernel.cu", 'r') as f:
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

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111)
fig.suptitle("Conway's Game of Life Accelerated with PyCUDA")
ax.set_title('Number of Iterations = %d' % (n_iter))
myobj = plt.imshow(C_gpu.get(), origin='lower', cmap='Greys',
                   interpolation='nearest', vmin=0, vmax=1)
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
