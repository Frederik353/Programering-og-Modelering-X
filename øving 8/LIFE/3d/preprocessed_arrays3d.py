import pycuda.autoinit
import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
import numpy as np
# from pylab import cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time
from adjecent_cells import get_neighbours

# n = 2 ** 12  # 4k
# n_iter = 10_00
n_iter = 0
ndim = 3

C = np.load("./bin/C.npy")
n = len(C)
M = np.load("./bin/M.npy")


n_block = 2**5
print(int(n/n_block))
n_grid = int(n/n_block)
# n = n_block*n_grid
m = n_iter



with open("./kernel3d.cu", 'r') as f:
    kernel = f.read()

mod = SourceModule(kernel)
func = mod.get_function("step")


C_gpu = gpuarray.to_gpu(C)
M_gpu = gpuarray.to_gpu(M)
Neigbors = get_neighbours(ndim)
Neigbor_count = len(Neighbours)
Neigbors_gpu = gpuarray.to_gpu(Neigbors)
Neigbor_count_gpu = gpuarray.to_gpu(Neigbor_count)
ndim_gpu = gpuarray.to_gpu(ndim)


def update(framenum, img, title, func):
    global n_block, n_grid, m,  C_gpu, M_gpu
    m += 1
    t1 = time()
    # print(t1 - t2)
    func(C_gpu, M_gpu, Neigbors_gpu, Neigbor_count_gpu, ndim_gpu,block=(n_block, n_block, 1), grid=(n_grid, n_grid, 1))
    foo = C_gpu
    C_gpu, M_gpu = M_gpu, C_gpu
    img.set_data(C_gpu.get())

    # print(C_gpu.get()[0][0])
    t2 = time()
    print(t2 - t1)

    # img.set_data(newGrid)
    # grid[:] = newGrid[:]
    title.set_text(f"Number of Iterations = {m}")
    return [img, title]



def main():
    global C_gpu, M_gpu

    for k in range(n_iter):
        func(C_gpu, M_gpu, block=(n_block, n_block, 1), grid=(n_grid, n_grid, 1))
        # C_gpu, M_gpu = M_gpu, C_gpu

    print("%d live cells after %d iterations" % (np.sum(C_gpu.get()), n_iter))

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    title = ax.text(0.16, 0.97, f"Number of Iterations = {m}", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                    transform=ax.transAxes, ha="center")

    img = ax.imshow(C_gpu.get(), origin='lower', cmap='Blues',
                    interpolation='nearest', vmin=0, vmax=1)

    fig.suptitle("Conway's Game of Life Accelerated with PyCUDA")

    # ani = animation.FuncAnimation(fig, update, fargs=( img, title, C_gpu, M_gpu, func), interval=0.0001, frames=10, save_count=50, blit=True)

    ani = animation.FuncAnimation(fig, update, fargs=(
        img, title, func), interval=0.00001, save_count=50,frames=50, blit=True)

    # set output file
    # f = r"./animation.gif"
    # writer = animation.FFMpegWriter(fps=60, bitrate=18000)
    # ani.save(f)

    plt.show()


if __name__ == '__main__':
    main()
