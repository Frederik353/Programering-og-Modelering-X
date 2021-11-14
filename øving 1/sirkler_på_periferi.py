import math
import numpy


for i in range(1000):
    N = math.pi / (numpy.arcsin((6.35) / (i*0.04 + 0.04)))
    # print(N, i)
    if not numpy.isnan(N):
        if N > round(N) + 0.2:
            print(N, (i*0.04 + 0.04))