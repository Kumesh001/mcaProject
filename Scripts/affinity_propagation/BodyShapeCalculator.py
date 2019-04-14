from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from itertools import cycle
import csv
import numpy as np

path='D:\others\MCA\SourceCode\mcaProject\data\output.csv'
# Make Dummy Data
centers = [[1, 1], [-1, -1], [1, -1]]
Y, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5, random_state=0)
X=[]
def loadFile():
        filepath=path
        with open(filepath) as f:
                reader = csv.reader(f)
                first_row = next(reader)
                for row in reader:
                        if len(row[0])!=0:
                                X.append(row)

loadFile() 
data=[]
for i in X:
        tempList=[]
        for j in i:
                tempList.append(float(j))
        data.append(tempList)

# Setup Affinity Propagation
Z = np.array(data)
af = AffinityPropagation(preference=-200).fit(Z)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

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
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
    for x in Z[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.show()