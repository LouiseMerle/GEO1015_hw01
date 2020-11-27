### just here ###
import sys
import csv
import json
#################

import math
import numpy
import scipy.spatial
import startin

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
        j_idw = jparams['idw']
        r = csv.reader(csvfile, delimiter=' ')
        header = next(r)
        for line in r:
            p = list(map(float, line)) #-- convert each str to a float
            assert(len(p) == 3)
            list_pts_3d.append(p)

    cellsize= j_idw['cellsize']
    radius = j_idw['radius']
    power = j_idw['power']

    x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)
    
    zip_list = list(zip(x_list_points, y_list_points))
    tree = scipy.spatial.KDTree(zip_list)

    ncols = math.ceil((max(x_list_points)-min(x_list_points) + (0.5 * cellsize))/cellsize) # (0.5 * cellsize) adds an additional col, even if max-min is divisible by cellsize
    nrows = math.ceil((max(y_list_points)-min(y_list_points) + (0.5 * cellsize))/cellsize)
    
    range_y = range(int(min(y_list_points)), int(nrows * cellsize + cellsize), int(cellsize))
    range_y1 = range(int(min(y_list_points)), int(max(y_list_points) + cellsize), int(cellsize))
    range_x = range(int(min(x_list_points)), int(max(x_list_points) + cellsize), int(cellsize))
    
    print(range_y)
    print(range_y1)

if __name__ == '__main__':
    main()

