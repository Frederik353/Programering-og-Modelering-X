import pycuda.autoinit
import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
# import sys
import numpy as np
# from pylab import cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time

# n = 2 ** 12  # 4k
# n_iter = 10_00
n_iter = 0


C = np.load("./LIFE/bin/C.npy")
n = len(C)
M = np.load("./LIFE/bin/M.npy")


n_block = 2**5
# n_block = 2*2
print(int(n/n_block))
n_grid = int(n/n_block)
n = n_block*n_grid

m = n_iter



with open("./LIFE/kernel2d.cu", 'r') as f:
    kernel = f.read()

mod = SourceModule(kernel)
func = mod.get_function("step")


C_gpu = gpuarray.to_gpu(C)
M_gpu = gpuarray.to_gpu(M)



def update(framenum, img, title, func):
    global n_block, n_grid, m,  C_gpu, M_gpu
    m += 1
    t1 = time()
    func(C_gpu, M_gpu, block=(n_block, n_block, 1), grid=(n_grid, n_grid, 1))
    # foo = C_gpu
    C_gpu, M_gpu = M_gpu, C_gpu
    img.set_data(C_gpu.get())

    t2 = time()
    print(t2 - t1)

    title.set_text(f"Number of Iterations = {m}")
    return [img, title]


def main():
    global C_gpu, M_gpu

    for k in range(n_iter):
        func(C_gpu, M_gpu, block=(n_block, n_block, 1), grid=(n_grid, n_grid, 1))

    print(f"{np.sum(C_gpu.get())} live cells after {n_iter} iterations")

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    title = ax.text(0.16, 0.97, f"Number of Iterations = {m}", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                    transform=ax.transAxes, ha="center")

    img = ax.imshow(C_gpu.get(), origin='lower', cmap='Blues',
                    interpolation='nearest', vmin=0, vmax=1)

    fig.suptitle("Conway's Game of Life Accelerated with PyCUDA")


    ani = animation.FuncAnimation(fig, update, fargs=(
        img, title, func), interval=0.00001, save_count=50,frames=50, blit=True)

    # set output file
    # f = r"./animation.gif"
    # writer = animation.FFMpegWriter(fps=60, bitrate=18000)
    # ani.save(f)

    plt.show()


if __name__ == '__main__':
    main()
