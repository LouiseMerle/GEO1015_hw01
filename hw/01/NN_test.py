import numpy
import scipy.spatial
import sys
import math
import csv
import random
import json 
import time
import copy 



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

def main():
    #-- read the needed parameters from the file 'params.json' (must be in same folder)
    try:
        jparams = json.load(open('params.json'))
    except:
        print("ERROR: something is wrong with the params.json file.")
        sys.exit()
    #-- store the input 3D points in list
    list_pts_3d = []
    with open(jparams['input-file']) as csvfile:
        j_nn = jparams['nn']
        r = csv.reader(csvfile, delimiter=' ')
        header = next(r)
        for line in r:
            p = list(map(float, line)) #-- convert each str to a float
            assert(len(p) == 3)
            list_pts_3d.append(p)

    # get cellsize from j_params file 
    cellsize= j_nn['cellsize']
   
    # split the list of 3d sample points in lists for x, y and z 
    x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)

    # create the KDTree with the x and y values of the sample points 
    zip_list = list(zip(x_list_points, y_list_points))
    tree = scipy.spatial.KDTree(zip_list) 

    # create convex hull
    hull = scipy.spatial.ConvexHull(zip_list)

    # calcalute number of rows and colums to wtrite in the asc file
    ncols = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
    nrows = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
    
    # make x and y ranges for the x and y axes for the bbox
    # add 1 cellsize ??????
    range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
    range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)
    
    # make list with all x y coordinates on the x and y axis of the raster
    coordinate_lst = [[x, y] for y in range_y for x in range_x]

    # query the raster coordinates with the sample points 
    for i in coordinate_lst:
        d, i_nn = tree.query(i,k=1)
        i.append(z_list_points[i_nn])

    row_nr = 0
    col_nr = 0
    with open('Swiss.asc', 'w') as fh:
        fh.writelines('NCOLS {}\n'.format(ncols))
        fh.writelines('NROWS {}\n'.format(nrows))
        fh.writelines('XLLCENTER {}\n'.format(min(x_list_points) + (0.5 * cellsize)))
        fh.writelines('YLLCENTER {}\n'.format(min(y_list_points) + (0.5 * cellsize)))
        fh.writelines('CELLSIZE {}\n'.format(j_nn['cellsize']))
        fh.writelines('NO_DATA VALUE -9999\n')
        
        for i in coordinate_lst:
            fh.write(str(i[-1])+' ')
            col_nr += 1
        
            if col_nr == ncols:
                col_nr = 0
                row_nr += 1
                fh.write('\n')
        
if __name__ == '__main__':
    main()