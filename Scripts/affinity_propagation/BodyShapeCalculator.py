from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from itertools import cycle
import csv
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import pandas as pd

path='G:/MCA Project/mcaProject/data/output.csv'
X=[]
def loadFile():
        filepath=path
        with open(filepath) as f:
                reader = csv.reader(f)
                first_row = next(reader)
                for row in reader:
                        if len(row)!=0:
                                X.append(row)
loadFile() 
data=[]
for i in X:
        tempList=[]
        for j in range(1,len(i)):
                tempList.append(float(i[j]))
        data.append(tempList)

# Setup Affinity Propagation
Z = np.array(data)
af = AffinityPropagation(preference=-200).fit(Z)
cluster_centers_indices = af.cluster_centers_indices_
print(cluster_centers_indices)
labels = af.labels_
# print(labels)

no_clusters = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % no_clusters)
# Plot exemplars

plt.close('all')
plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(no_clusters), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    plt.plot(Z[class_members, 0], Z[class_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=8)
    for x in Z[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)
plt.show()