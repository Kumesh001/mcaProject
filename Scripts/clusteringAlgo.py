import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

n = 20
size = (n, 2)
np.random.seed(3)
x = np.random.normal(0, 1, size)

def similarity(xi, xj):
    return -((xi - xj)**2).sum()

def create_matrices():
    S = np.zeros((x.shape[0], x.shape[0]))
    R = np.array(S)
    A = np.array(S)
    
    # compute similarity for every data point.
    for i in range(x.shape[0]):
        for k in range(x.shape[0]):
            S[i, k] = similarity(x[i], x[k])
            
    return A, R, S

for i in range(4):
    center = np.random.rand(2) * 10
    x = np.append(x, np.random.normal(center, .5, size), axis=0)
    c = [c for s in [v * n for v in 'bgrcmyk'] for c in list(s)]
    plt.figure(figsize=(15, 6)) 
    plt.title('Some clusters in 2d space')
    plt.scatter(x[:, 0], x[:, 1], c=  plt.show())