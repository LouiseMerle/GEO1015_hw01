from scipy import spatial

import sys
import math
import csv
import random
import json 
import time

import math
import numpy
import scipy.spatial
#import startin 



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

j_nn = jparams['nn']

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

def gridding():
    min_coordinate, max_coordinate = bbox(list_pts_3d, j_nn['cellsize']) 
    x_axis = numpy.arange(min_coordinate[0], max_coordinate[0], j_nn['cellsize'])
    y_axis = numpy.arange(min_coordinate[1], max_coordinate[1], j_nn['cellsize'])
    #x_grid, y_grid = numpy.meshgrid(x_axis, y_axis, sparse=True)
    return x_axis, y_axis

bounding_box = bbox(list_pts_3d, j_nn['cellsize'])

x_axis, y_axis = gridding()
x_flip = numpy.flip(x_axis)
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
            query_point = (x_flip[i], y_axis[j])
            d, i_nn = tree.query(query_point, k=1)
            z_value = z_list_points[i_nn]
            z_rast[i][j] = z_value

    for line in z_rast:
        numpy.savetxt(fh, line, fmt='%.4f')