### just here ###
import sys
import csv
import json
#################

import math
import numpy
import scipy.spatial
import startin


# split 3d points list in separate lists for x y and z
def split_xyz(point_list3d): 
    x = [point[0] for point in point_list3d]
    y = [point[1] for point in point_list3d]
    z = [point[2] for point in point_list3d]
    return x, y, z

# function to calculate the distance between a sample and a raster point
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
        j_kriging = jparams['kriging']
        r = csv.reader(csvfile, delimiter=' ')
        header = next(r)
        for line in r:
            p = list(map(float, line)) #-- convert each str to a float
            assert(len(p) == 3)
            list_pts_3d.append(p)

    cellsize= j_kriging['cellsize']
    radius = j_kriging['radius']

    # Remove duplicate points
    clean_points_list = []
    for point1 in list_pts_3d:
        repeated = False
        for point2 in clean_points_list:
            if point1[0] == point2[0] and point1[1] == point2[1]:
                repeated = True
        if repeated == False:
            clean_points_list.append(point1)
        else:
            print("Repeated point: " + str(point1[0]) + " " + str(point1[1]))
    #points = np.array(clean_points_list)       # --> numpy array of any adventage?


    # split the cleaned list of 3d sample points in lists for x, y and z 
    x_list_points, y_list_points, z_list_points = split_xyz(clean_points_list)

    # create the KDTree with the x and y values of the sample points 
    xy_list = list(zip(x_list_points, y_list_points))
    tree = scipy.spatial.KDTree(xy_list) 

    # calcalute number of rows and colums to wtrite in the asc file
    ncols = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
    nrows = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
    
    # make x and y ranges for the x and y axes for the bbox
    # add 0.5 cellsize to find the centre points of the 
    range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
    range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)
    
    # make list with all x y coordinates on the x and y axis of the raster
    coordinate_lst = [[x, y] for y in range_y for x in range_x]

    def cellvalue_kriging (raster_point, r):
        ''' raster_point: point for that the new value is determined
            r: radius around raster_point within nearby sample points are used for interpolation
        '''

        # i_kriging list of indicies with points within radius
        i_kriging = kd_tree.query_ball_point(raster_point, r)       

        # return none value if no point is found within the radius
        if len(i_kriging) == 0:
            return -9999