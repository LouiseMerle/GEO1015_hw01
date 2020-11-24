from scipy import spatial
###
import sys
import math
import csv
import random
import json 
import time

import math
import numpy
import scipy.spatial
import startin 

from matplotlib import pyplot as plt

try:
    jparams = json.load(open('params.json'))
except:
    print("ERROR: something is wrong with the params.json file.")
    sys.exit()
#-- store the input 3D points in list
list_pts_3d = []
with open(jparams['input-file']) as csvfile:
    r = csv.reader(csvfile, delimiter=' ')
    header = next(r)
    for line in r:
        p = list(map(float, line)) #-- convert each str to a float
        assert(len(p) == 3)
        list_pts_3d.append(p)
#print(list_pts_3d)
#-- interpolations if in the params
#if 'nn' in jparams:
 #   start_time = time.time()
 #   print("=== Nearest neighbour interpolation ===")
  #  my_code_hw01.nn_interpolation(list_pts_3d, jparams['nn'])
  #  print("-->%ss" % round(time.time() - start_time, 2))


print(jparams['nn']['cellsize'])

j_nn = jparams['nn']

def nn_interpolation(list_pts_3d, j_nn):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with nearest neighbour interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_nn:        the parameters of the input for "nn"
    Output:
        returns the value of the area
 
    """  
    # print("cellsize:", j_nn['cellsize'])

    #-- to speed up the nearest neighbour us a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    # kd = scipy.spatial.KDTree(list_pts)
    # d, i = kd.query(p, k=1)

    print("File written to", j_nn['output-file'])

def split_xyz(point_list3d):
    x_list = []
    y_list = []
    z_list = []
    for points in point_list3d: 
        x = points[0]
        x_list.append(x)
        y = points[1]
        y_list.append(y)
        z = points[2]
        z_list.append(z)
    return x_list, y_list, z_list

def bbox(point_list, cell_size=1):
    x_list, y_list, _ = split_xyz(point_list)
    
    min_coordinate = (min(x_list), min(y_list))
    max_coordinate = (max(x_list), max(y_list))

    height_bb = max_coordinate[1] - min_coordinate[1]
    width_bb = max_coordinate[0] - min_coordinate[0]

    if height_bb % cell_size == 0 and width_bb % cell_size == 0:
        return min_coordinate, max_coordinate
    elif height_bb % cell_size == 0 and width_bb % cell_size != 0:
        num_cells_x = max_coordinate[0] // cell_size
        new_width = (num_cells_x + 1) * cell_size 
        new_max_x = min_coordinate[0] + new_width
        max_coordinate_new = (new_max_x, max_coordinate[1])
        return min_coordinate, max_coordinate_new
    elif height_bb % cell_size != 0 and width_bb % cell_size == 0:
        num_cells_y = max_coordinate[1] // cell_size
        new_width = (num_cells_y + 1) * cell_size 
        new_max_y = min_coordinate[1] + new_width
        max_coordinate_new = (max_coordinate, new_max_y)
        return min_coordinate, max_coordinate_new
    else: 
        num_cells_x = max_coordinate[0] // cell_size
        new_width = (num_cells_x + 1) * cell_size 
        new_max_x = min_coordinate[0] + new_width
        num_cells_y = max_coordinate[1] // cell_size
        new_width = (num_cells_y + 1) * cell_size 
        new_max_y = min_coordinate[1] + new_width
        max_coordinate_new = (new_max_x, new_max_y)
        return min_coordinate, max_coordinate_new


#min_coordinate, max_coordinate = bbox(list_pts_3d, j_nn['cellsize'])

#print('min', min_coordinate)
#print('max', max_coordinate)

'''
first we make the grid

kd tree with x and y 

query the tree to get z value for each cell 
'''

'''
def gridding():
    min_coordinate, max_coordinate = bbox(list_pts_3d, j_nn['cellsize']) 
    x_axis = []
    y_axis = []
    for i in numpy.arange(min_coordinate[0], max_coordinate[0] + j_nn['cellsize'], j_nn['cellsize']):
        if i <= max_coordinate[0]:
            x_axis.append(i)

    for i in numpy.arange(min_coordinate[1], max_coordinate[1] + j_nn['cellsize'], j_nn['cellsize']):
        if i <= max_coordinate[1]:
            y_axis.append(i)

    grid = numpy.meshgrid(x_axis, y_axis)
    return grid


def gridding():
    min_coordinate, max_coordinate = bbox(list_pts_3d, j_nn['cellsize']) 
    x_axis = numpy.arange(min_coordinate[0], max_coordinate[0] + j_nn['cellsize'], j_nn['cellsize'])
    y_axis = numpy.arange(min_coordinate[1], max_coordinate[1] + j_nn['cellsize'], j_nn['cellsize'])
    #x_grid, y_grid = numpy.meshgrid(x_axis, y_axis, sparse=True)
    return x_axis, y_axis
'''
bounding_box = bbox(list_pts_3d, j_nn['cellsize'])

def gridding():
    min_coordinate, max_coordinate = bbox(list_pts_3d, j_nn['cellsize']) 
    x_axis = numpy.arange(min_coordinate[0], max_coordinate[0], j_nn['cellsize'])
    y_axis = numpy.arange(min_coordinate[1], max_coordinate[1], j_nn['cellsize'])
    #x_grid, y_grid = numpy.meshgrid(x_axis, y_axis, sparse=True)
    return x_axis, y_axis

x_axis, y_axis = gridding()

y_flip = numpy.flip(y_axis)

x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)

zip_list = list(zip(x_list_points, y_list_points))
tree = spatial.KDTree(zip_list)

print(tree.data)

z_rast = numpy.zeros((x_axis.shape[0], y_axis.shape[0]))

with open('test.asc', 'w') as fh:
    fh.write('NCOLS {}\n'.format(x_axis.shape[0]))
    fh.write('NROWS {}\n'.format(y_axis.shape[0]))
    fh.write('XLLCORNER {}\n'.format(bounding_box[0][0]))
    fh.write('YLLCORNER {}\n'.format(bounding_box[0][1]))
    fh.write('CELLSIZE {}\n'.format(j_nn['cellsize']))
    fh.write('NODATA_VALUE -9999\n')

    for j in range(y_axis.shape[0]):
        for i in range(x_axis.shape[0]):
            query_point = (x_axis[i], y_flip[j])
            d, i_nn = tree.query(query_point, k=1)
            z_value = z_list_points[i_nn]
            z_rast[i][j] = z_value

    for line in z_rast:
        numpy.savetxt(fh, line, fmt='%.4f')
    
print("File written to", j_nn['output-file'])


#z_rast = numpy.zeros_like(x_grid)

'''
for j in range(x_grid.shape[0]):
    print(j)
    for i in range(x_grid.shape[1]):
        print(i)
        query_point = (x_grid[j][i], y_grid[j][i])
        d, i_nn = tree.query(query_point, k=1)
        print(i_nn)
        z_value = z_list_points[i_nn]
        z_rast[i][j] = z_value


fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(x_grid, y_grid, z_rast, rstride=1, cstride=1)
plt.show()




for y_value in numpy.flip(y_axis):
        z_list = []
        for x_value in x_axis:
            query_point = (x_value, y_value)
            #print(query_point)
            d, i_nn = tree.query(query_point, k=1)
            z_value = z_list_points[i_nn]
            z_list.append(z_value)
'''