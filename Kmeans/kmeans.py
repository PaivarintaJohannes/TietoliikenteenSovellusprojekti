import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

## Määritellään data yms
data = np.genfromtxt('data1.csv',delimiter=',')
coordinates = data[:,1:]
direction_ids = data[:,0]
numberOfRows = coordinates.shape[0]
numberOfRows = int(numberOfRows)
max_values = np.max(coordinates, axis=0)
centerPointCumulativeSum = np.zeros((6,3))
counts = np.zeros((1,6))
new_centers = np.zeros((6,3))
amountOfCenters = 6

##randompointtien määrittely
def kMeansPlusPlusInit(data, k):
    centers = np.zeros((k, data.shape[1]))
    centers[0] = data[np.random.choice(data.shape[0])]
    
    for i in range(1, k):
        distances = np.array([min(np.linalg.norm(x - center) for center in centers[:i]) for x in data])
        probabilities = distances**2 / np.sum(distances**2)
        centers[i] = data[np.random.choice(data.shape[0], p=probabilities)]
    
    return centers
##debuggaamiseen
def debugPrints():
    print("numberOfRows = ", numberOfRows)
    print("data = \n",data)
    print("k_centers = \n", k_centers)
    print("centerPointCumulativeSum = \n",centerPointCumulativeSum)
    print("new_centers = \n",new_centers)
k_centers = kMeansPlusPlusInit(coordinates, amountOfCenters)
def plottaus():
    fig = plt.figure()
    colors = plt.cm.rainbow(direction_ids / direction_ids.max())
    ax = fig.add_subplot(111, projection='3d')
    for i in range(6):
        ax.scatter(new_centers[i,0],new_centers[i,1],new_centers[i,2], c='black', marker='x', label='Calculated Centers' if i == 0 else '')
    for i in range(6):
        ax.scatter(k_centers[i,0],k_centers[i,1],k_centers[i,2], c='b', marker='o',label='Random Points' if i == 0 else '')
    for direction_id in np.unique(direction_ids):
        indices = direction_ids == direction_id
        ax.scatter(coordinates[indices, 0], coordinates[indices, 1], coordinates[indices, 2], c=colors[indices],
                   marker='o', label=f'Suunta id {int(direction_id)}')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()

def calculateNewCenters():
    for i in range(amountOfCenters):
        if counts[0, i] != 0:
            new_centers[i, :] = centerPointCumulativeSum[i, :] / counts[0, i]
        else:          
            new_centers[i, :] = k_centers[i, :]

## Määritellään suunnat keskipisteille
def suunnat():
    direction_ids_for_clusters = np.zeros(amountOfCenters, dtype=int)
    for cluster_index in range(amountOfCenters):
        indices_in_cluster = np.where(assigned_clusters == cluster_index)[0]
        if len(indices_in_cluster) > 0:
            direction_id_for_cluster = direction_ids[indices_in_cluster].astype(int)
            most_frequent_direction_id = np.argmax(np.bincount(direction_id_for_cluster))
            direction_ids_for_clusters[cluster_index] = most_frequent_direction_id
    for cluster_index, direction_id in enumerate(direction_ids_for_clusters):
        center = new_centers[cluster_index, :]
        print(f"Suunta{direction_id}_center: {center}")
## Tarkistetaan että countit on ok
def checkZeros():
    if np.any(counts == 0):         
        zero_index = np.where(counts == 0)[0][0]
        k_centers[zero_index, :] = np.random.rand(3) * max_values 
        kMeans()    
    else:
       calculateNewCenters()
## ite pää-funktio
def kMeans():
    
    for i in range(numberOfRows):
        datapoint = coordinates[i,:]
        distances = np.zeros((1, 6))
        for j in range(6):
            distances[0, j] = np.linalg.norm(datapoint - k_centers[j,:])     
        winner = np.argmin(distances)
        centerPointCumulativeSum[winner,:] += datapoint
        counts[0,winner] += 1
    
    checkZeros()
      

for i in range(10):
   kMeans()
assigned_clusters = np.argmin(np.linalg.norm(coordinates - new_centers[:, np.newaxis, :], axis=2), axis=0)

plottaus()
##print(counts)
suunnat()



