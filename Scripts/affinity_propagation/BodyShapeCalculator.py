from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from itertools import cycle
import csv
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import pandas as pd

path='G:/MCA Project/mcaProject/data/output.csv'
# Make Dummy Data
# centers = [[1, 1], [-1, -1], [1, -1]]
# Y, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5, random_state=0)
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
af = AffinityPropagation(preference=-3000).fit(Z)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

no_clusters = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % no_clusters)
# Plot exemplars

plt.close('all')
plt.figure(1)
plt.clf()

X_embedded = TSNE(n_components=2).fit_transform(Z)
print(X_embedded.shape)
# pca = PCA(n_components=2)
# principalComponents = pca.fit_transform(Z)
# principalDf = pd.DataFrame(data = principalComponents
#              , columns = ['principal component 1', 'principal component 2'])

# finalDf = pd.concat([principalDf, df[['target']]], axis = 1)
# fig = plt.figure(figsize = (8,8))
# ax = fig.add_subplot(1,1,1) 
# ax.set_xlabel('Principal Component 1', fontsize = 15)
# ax.set_ylabel('Principal Component 2', fontsize = 15)
# ax.set_title('2 component PCA', fontsize = 20)
# targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
# colors = ['r', 'g', 'b']
# for target, color in zip(targets,colors):
#     indicesToKeep = finalDf['target'] == target
#     ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
#                , finalDf.loc[indicesToKeep, 'principal component 2']
#                , c = color
#                , s = 50)
# ax.legend(targets)
# ax.grid()

# colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
# for k, col in zip(range(no_clusters), colors):
#     class_members = labels == k
#     print()
#     print(Z[class_members, 0])
# #     maxval=max(Z[class_members, 0])
# #     print(maxval)
# #     minVal=min(Z[class_members, 1])
# #     print(minVal)
#     cluster_center = X[cluster_centers_indices[k]]
#     plt.plot(Z[class_members, 0], Z[class_members, 1], col + '.')
#     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=8)
#     for x in Z[class_members]:
#         plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.plot(X_embedded,'.')
plt.show()