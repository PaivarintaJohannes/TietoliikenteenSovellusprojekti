TVT22SPL Tietoliikenteen sovellusprojekti. Päivärinta, Kokko

# K-Means Algorithm
![Havainnollistus](https://github.com/PaivarintaJohannes/TietoliikenteenSovellusprojekti/blob/K-means/Kmeans/havainnollistus.png)
## Overview

This script demonstrates the K-Means algorithm, used for grouping data points into K clusters. The algorithm iteratively refines cluster centers based on the average position of data points within each cluster.

## Usage

1. **Data Loading:** The script loads a dataset from the 'putty.log' file. Ensure the file is available and formatted correctly.

2. **Initialization:** Random cluster centers are initialized within the data space.

3. **Clustering:** The K-Means algorithm is applied iteratively for a set number of times (100 in this case). It calculates distances between data points and cluster centers, assigns points to the nearest cluster, and updates the cluster centers.

4. **Visualization:** The results are visualized in a 3D plot using matplotlib. The calculated cluster centers are shown in green, the initial random points in blue, and the data points in red.

## Dependencies

- Python
- NumPy
- Matplotlib

## Saved center points
Suunta1: X:1479 Y:1501 Z:1788 (vaaka ylös)
Suunta2: X:1776 Y:1473 Z:1492 (vaaka alas)
Suunta3: X:1456 Y:1493 Z:1198 (sivuttain x:n sivu ylös)
Suunta4: X:1486 Y:1769 Z:1468 (alas)
Suunta5: X:1476 Y:1176 Z:1494 (ylös)
