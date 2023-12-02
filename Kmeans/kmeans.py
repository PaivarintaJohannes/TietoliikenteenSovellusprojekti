import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

## Määritellään data yms
data = np.genfromtxt('data.csv',delimiter=',')

coordinates = np.zeros((250,3))

direction_ids = data[:,0]
coordinates = data[:,1:]

numberOfRows = coordinates.shape[0]
numberOfRows = int(numberOfRows)
max_values = np.max(coordinates, axis=0)
centerPointCumulativeSum = np.zeros((5,3))
counts = np.zeros((1,5))
new_centers = np.zeros((5,3))
amountOfCenters = 5
distances = np.zeros((1, 5))
k_centers = coordinates[np.random.choice(numberOfRows, size=amountOfCenters, replace=False)]


##debuggaamiseen
def debugPrints():
    print("numberOfRows = ", numberOfRows)
    print("data = \n",data)
    print("k_centers = \n", k_centers)
    print("centerPointCumulativeSum = \n",centerPointCumulativeSum)
    print("new_centers = \n",new_centers)

def plottaus():
    fig = plt.figure()
    colors = plt.cm.rainbow(direction_ids / direction_ids.max())
    ax = fig.add_subplot(111, projection='3d')
    for i in range(5):
        ax.scatter(new_centers[i,0],new_centers[i,1],new_centers[i,2], c='black', marker='X', label='Calculated Centers' if i == 0 else '')
    for i in range(5):
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


def checkZeros():
    if np.any(counts == 0): 
        zero_index = np.where(counts == 0)[0][0]
        k_centers[zero_index, :] = np.random.rand(3) * max_values 
        kMeans()
    else:
       calculateNewCenters()

def kMeans():
    for i in range(numberOfRows):
        datapoint = coordinates[i,:]
        distances = np.zeros((1, 5))
        for j in range(5):
            distances[0, j] = np.linalg.norm(datapoint - k_centers[j,:])     
        winner = np.argmin(distances)
        centerPointCumulativeSum[winner,:] += datapoint
        counts[0,winner] += 1
    checkZeros()
      

for i in range(10):
    kMeans()
    

plottaus()
print(new_centers)


  

