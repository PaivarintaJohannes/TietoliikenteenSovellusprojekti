import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

## Määritellään data yms
data = np.loadtxt('putty.log')
data = data.reshape(40, 3)
numberOfRows = data.shape[0]
numberOfRows = int(numberOfRows)
max_values = np.max(data)
k_centers = np.random.rand(4, 3) * max_values
centerPointCumulativeSum = np.zeros((4,3))
counts = np.zeros((1,4))
new_centers = np.zeros((4,3))
amountOfCenters = 4

##debuggaamiseen
def debugPrints():
    print("numberOfRows = ", numberOfRows)
    print("data = \n",data)
    print("k_centers = \n", k_centers)
    print("centerPointCumulativeSum = \n",centerPointCumulativeSum)
    print("new_centers = \n",new_centers)

def plottaus():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(4):
        ax.scatter(new_centers[i,0],new_centers[i,1],new_centers[i,2], c='g', marker='o', label='Calculated Centers')
    for i in range(4):
        ax.scatter(k_centers[i,0],k_centers[i,1],k_centers[i,2], c='b', marker='o',label='Random Points For The Algorithm' if i == 0 else '')
    for i in range(40):
        ax.scatter(data[i,0],data[i,1],data[i,2], c='r', marker='o', label='Data Points' if i == 0 else '')
    
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
    zero_indices = np.where(counts == 0)[1]
    for zero_index in zero_indices:
        k_centers[zero_index, :] = np.random.rand(3) * max_values 




def kMeans():   
    for i in range(numberOfRows):
        datapoint = data[i, :]
        distances = np.zeros((1, 4))
        for j in range(4):
            distances[0, j] = np.linalg.norm(datapoint - k_centers[j, :])     
        winner = np.argmin(distances)
        centerPointCumulativeSum[winner, :] += datapoint
        counts[0, winner] += 1


for i in range(100):
    kMeans()
    checkZeros()


calculateNewCenters()

plottaus()
print(counts)
print(new_centers)

  

