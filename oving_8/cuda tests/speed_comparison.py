import numpy as np
import pycuda.autoinit
from pycuda import gpuarray
from time import time
host_data = np.float32(np.random.random(50000000))

for i in range(10):
    tc1 = time()
    host_data_2x = host_data * np.float32(2)
    tc2 = time()

    # print('total time to compute on CPU: %f' % (t2 - t1))
    device_data = gpuarray.to_gpu(host_data)

    device_data_2x = device_data * np.float32(2)
    tg1 = time()
    device_data_2x = device_data * np.float32(2)
    tg2 = time()

    from_device = device_data_2x.get()
    print(f"GPU: {tg2 -tg1} CPU: {tc2 -tc1}")
    # print('total time to compute on GPU: %f' % (t2 - t1))

    # print('Is the host computation the same as the GPU computation? : {}'.format( np.allclose(from_device, host_data_2x)))
