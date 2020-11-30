### just here ###
import sys
import csv
import json
#################

import math
import numpy
import scipy.spatial
import startin

cellsize = 2.0
x_list_points = [2.0, 3.8, 11.5, 8.9, 7.6, 6.1, 4.4, 10.7]
y_list_points = [3.0, 7.7, 8.2, 5.6, 4.9, 3.1, 6.4, 5.8]
z_list_points = [50, 40, 10, 20, 50, 20, 30, 10]

id_list = [1,3,4,6,7]
weight_list = [1, 0.5, 3, 0.25, 1]

point_list = []
for i in id_list:
    point_list.append(z_list_points[i])


s = 0
for num1, num2 in zip(weight_list, point_list):
	s += num1 * num2


# function to calculate the distance between a sample and a raster point
def distance(point_sample, point_raster):
    dx = point_sample[0] - point_raster[0]
    dy = point_sample[1] - point_raster[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance

# theoretical variogram (gaussian)
def variogram(distance):
    return 2 + 1400*(1.0 - math.exp(-9.0 * distance * distance / (300*300)))
    # nugget_gaussian+sill_gaussian*(1.0 - math.exp(-9.0*bin*bin/(range_gaussian*range_gaussian)))


neighbour_points = [(235.0, 215.0), (240.0, 186.0), (129.0, 64.0)]

A_matrix = []
for point in neighbour_points:
    row =[]
    for other_point in neighbour_points:
        dist = distance(point, other_point)
        gamma = variogram(dist)
        row.append(gamma)
    A_matrix.append(row)

print(A_matrix)