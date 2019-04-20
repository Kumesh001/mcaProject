import cv2
import numpy as np
from sklearn.cluster import KMeans

imagePath='G:/MCA Project/mcaProject/data/Images/testImages'

def generate_color_histogram(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    histgrm = cv2.calcHist([image], [0,1,2], None, [8,12,3], [0,180,0,256,0,256])
    histgrm = cv2.normalize(histgrm, histgrm).flatten()
    return histgrm

def features(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    extractor = cv2.xfeatures2d.SIFT_create(20)
    keypoints, descriptors = extractor.detectAndCompute(image, None)
    return keypoints, descriptors

def build_histogram(descriptor_list, cluster_alg):
    histogram = np.zeros(len(cluster_alg.cluster_centers_))
    cluster_result =  cluster_alg.predict(descriptor_list)
    for i in cluster_result:
        histogram[i] += 1.0
    return histogram

def generate_bov_histogram(image):
    preprocessed_image = []
    keypoint, descriptor = features(image)
    if (descriptor is not None):
        kmeans = KMeans(n_clusters = 7)
        kmeans.fit(descriptor)
        histogram = build_histogram(descriptor, kmeans)
        preprocessed_image.append(histogram)
    return preprocessed_image;



image = cv2.imread(imagePath+'/'+'a.jpg')
color_hist = generate_color_histogram(image)
#print(color_hist)
bov_hist = generate_bov_histogram(image)
print(bov_hist)

complete_hist = []
complete_hist.extend(color_hist)
complete_hist.extend(bov_hist[0])
print(complete_hist)


