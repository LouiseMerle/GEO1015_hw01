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

print(jparams['nn']['cellsize'])

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

x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)

ncols = int((max(x_list_points)-min(x_list_points))/j_nn['cellsize'])
nrows = int((max(y_list_points)-min(y_list_points))/j_nn['cellsize'])

x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)

yrange = reversed(range(int(min(y_list_points) + (0.5 * j_nn['cellsize'])), int(max(y_list_points) + (1.5 * j_nn['cellsize'])), j_nn['cellsize']))
xrange = (range(int(min(x_list_points)+ (0.5 * j_nn['cellsize'])), int(max(x_list_points) + (1.5 * j_nn['cellsize'])), j_nn['cellsize']))

coordinates = [[i, j] for j in yrange for i in xrange]

zip_list = list(zip(x_list_points, y_list_points))
tree = spatial.KDTree(zip_list)

z_rast = numpy.zeros((ncols, nrows))
#z_val_list= []

with open('test.asc', 'w') as fh:
    fh.write('NCOLS {}\n'.format(ncols))
    fh.write('NROWS {}\n'.format(nrows))
    fh.write('XLLCORNER {}\n'.format(min(x_list_points), min(y_list_points)))
    fh.write('YLLCORNER {}\n'.format(max(x_list_points), max(y_list_points)))
    fh.write('CELLSIZE {}\n'.format(j_nn['cellsize']))
    fh.write('NODATA_VALUE -9999\n')

    i = 0 
    for query_point in coordinates:
        d, i_nn = tree.query(query_point, k=1)
        z_value = z_list_points[i_nn]
        fh.write(str(z_value) + ' ')

        i += 1 
        if i == ncols:
            fh.write('\n')
            i = 0

            #z_val_list.append(z_value)
            #z_array = numpy.array(z_val_list)
    
    #numpy.savetxt(fh, z_array, fmt='%.4f')