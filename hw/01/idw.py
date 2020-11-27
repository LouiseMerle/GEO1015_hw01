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

    # calcalute number of rows and colums to wtrite in the asc file
    ncols = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
    nrows = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
    
    # make x and y ranges for the x and y axes for the bbox
    # add 0.5 cellsize to find the centre points of the 
    range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
    range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)
    
    # make list with all x y coordinates on the x and y axis of the raster
    coordinate_lst = [[x, y] for y in range_y for x in range_x]
    
    def distance (p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

    def cellvalue_idw (point, r, p):               # point is centerpoint of cell
        i_idw = tree.query_ball_point(point, r)        # i_idw list of indicies with points within radius

        if len(i_idw) == 0:
            return -9999

        weight_list = []
        for i in i_idw:
            d = distance(point, zip_list[i])
            w_i = 1/d ** p
            weight_list.append(w_i)
        
        #if sum(weight_list) == 'inf':
            #return -9999
        
        point_list = []
        for i in i_idw:
            point_list.append(z_list_points[i])
        s = 0
        for num1, num2 in zip(weight_list, point_list):
            s += num1 * num2
        
        if s/sum(weight_list) == 'inf':
            return -9999

        return(s/sum(weight_list))
        
    raster_values = []

    for i in coordinate_lst:
        raster_values.append(cellvalue_idw(i, radius, power))
        
    row_nr = 0
    col_nr = 0
    with open('sample_idw.asc', 'w') as fh:
        fh.writelines('NCOLS {}\n'.format(ncols))
        fh.writelines('NROWS {}\n'.format(nrows))
        fh.writelines('XLLCENTER {}\n'.format(min(x_list_points) + (0.5 * cellsize)))
        fh.writelines('YLLCENTER {}\n'.format(min(y_list_points) + (0.5 * cellsize)))
        fh.writelines('CELLSIZE {}\n'.format(j_idw['cellsize']))
        fh.writelines('NO_DATA VALUE -9999\n')
        
        for i in raster_values:
            fh.write(str(i)+' ')
            col_nr += 1
        
            if col_nr == ncols:
                col_nr = 0
                row_nr += 1
                fh.write('\n')

if __name__ == '__main__':
    main()

