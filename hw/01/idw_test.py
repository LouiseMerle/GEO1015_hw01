import math
import numpy

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
    
print (s)
#print(sum(products))












ncols1 = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
ncols = math.ceil((max(x_list_points)-min(x_list_points) + (0.5 * cellsize))/cellsize)
print(ncols1)
print(ncols)

nrows1 = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
nrows = math.ceil((max(y_list_points)-min(y_list_points) + (0.5 * cellsize))/cellsize)

print(nrows1)
print(nrows)

#range_x1 = range(int(min(x_list_points)), int(ncols * cellsize + cellsize), int(cellsize))

#range_x = range(int(min(x_list_points)), int(max(x_list_points) + cellsize), int(cellsize))
#range_y = reversed(range(int(min(y_list_points)), int(max(y_list_points) + cellsize), int(cellsize)))


# make x and y ranges for the x and y axes for the bbox
# add 0.5 cellsize to find the centre points of the 
range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)

#print(range_x1)
#print(range_x)

coordinate_lst = [[x, y] for y in range_y for x in range_x] # for ll of each cell or centerpoint??
#print(coordinate_lst)
