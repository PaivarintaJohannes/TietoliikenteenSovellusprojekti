import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

data = np.loadtxt('putty.log')

numberOfRows = data.shape[0]

max_values = np.max(data, axis=0)
k_centers = np.random.rand(4, 3) * max_values
data = data.reshape(40, 3)

centerPointCumulativeSum = np.zeros((4,3))

distances = np.zeros((1,4))
counts = np.zeros((1,4))

for i in range(40):
    datapoint = data[i,:]

    for j in range(4):
        distances[0, j] = np.linalg.norm(datapoint - k_centers[:])
        winner = np.argmin(distances)
        centerPointCumulativeSum[winner,:] += datapoint
        counts[0,winner] += 1

print(winner)
uudetKeskiPisteet = np.zeros((4,3))

if np.any(counts == 0): 
        zero_index = np.where(counts == 0)[0][0]
        k_centers[zero_index, :] = np.random.rand(3) * max_values


for i in range(4):
    uudetKeskiPisteet[i, :] = centerPointCumulativeSum[i, :] / counts[0, i]

print(uudetKeskiPisteet)
print(counts)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(4):
    ax.scatter(uudetKeskiPisteet[i,0], uudetKeskiPisteet[i, 1], uudetKeskiPisteet[i, 2], c='g', marker='o')

for i in range(40):
    ax.scatter(data[i,0],data[i,1],data[i,2], c='r', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()



