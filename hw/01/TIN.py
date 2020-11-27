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

def distance(point_sample, point_raster):
    dx = point_sample[0] - point_raster[0]
    dy = point_sample[1] - point_raster[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance

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
        j_tin = jparams['tin']
        r = csv.reader(csvfile, delimiter=' ')
        header = next(r)
        for line in r:
            p = list(map(float, line)) #-- convert each str to a float
            assert(len(p) == 3)
            list_pts_3d.append(p)


# Start TIN 
    cellsize = j_tin['cellsize']
   
    # split the list of 3d sample points in lists for x, y and z 
    x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)

    # create list with x and y values of 3d points list 
    xy_list = list(zip(x_list_points, y_list_points))

    # calcalute number of rows and colums to wtrite in the asc file
    ncols = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
    nrows = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
    
    # make x and y ranges for the x and y axes for the bbox
    # add 0.5 cellsize to find the centre points of the 
    range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
    range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)
    
    # make list with all x y coordinates on the x and y axis of the raster
    coordinate_lst = [[x, y] for y in range_y for x in range_x]
    print(coordinate_lst)
    
    # convex hull
    # used for triangulation
    hull = scipy.spatial.Delaunay(xy_list)
    
    # find 
    for raster_point in coordinate_lst:
        simplex = hull.find_simplex(raster_point)
        vertices = hull.vertices[simplex]

        if simplex == -1:
            raster_point.append(-9999)
        else: 
            # find point on raster with index of vertices
            p1 = coordinate_lst[vertices[0]]
            p2 = coordinate_lst[vertices[1]]
            p3 = coordinate_lst[vertices[2]]

            # test if vertex is the raster point
            if distance(p1, raster_point) == 0:
                z_value = z_list_points[vertices[0]]
                raster_point.append(z_value)
            elif distance(p2, raster_point) == 0:
                z_value = z_list_points[vertices[1]]
                raster_point.append(z_value)
            elif distance(p3, raster_point) == 0:
                z_value = z_list_points[vertices[2]]
                raster_point.append(z_value)
            else:
                # define weights for distance to points 
                w1 = 1 / distance(p1, raster_point)
                w2 = 1 / distance(p2, raster_point)
                w3 = 1 / distance(p3, raster_point)

            # calculate z value 
            z_value = (w1 * z_list_points[vertices[0]] + w2 * z_list_points[vertices[1]] + w3 * z_list_points[vertices[2]]) / (w1 + w2 + w3)

            # append z value to raster point coordinates
            raster_point.append(z_value)

    # count row and column numbers to write row by row in asc file 
    row_nr = 0
    col_nr = 0

    # open asc output file and write 
    with open('test_tin.asc', 'w') as fh:
        fh.write('NCOLS {}\n'.format(ncols))
        fh.write('NROWS {}\n'.format(nrows))
        fh.write('XLLCENTER {}\n'.format(min(x_list_points) + (0.5 * cellsize)))
        fh.write('YLLCENTER {}\n'.format(min(y_list_points) + (0.5 * cellsize)))
        fh.write('CELLSIZE {}\n'.format(j_tin['cellsize']))
        fh.write('NODATA_VALUE {}\n'.format(-9999))

        # write z values in asc file jn
        for point in coordinate_lst:
            fh.write(str(point[-1])+' ')
            col_nr += 1
        
            # print new line charater when nr of colls is reached and row is full
            if col_nr == ncols:
                col_nr = 0
                row_nr += 1
                fh.write('\n')

if __name__ == '__main__':
    main()