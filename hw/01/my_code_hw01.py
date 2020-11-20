#-- my_code_hw01.py
#-- hw01 GEO1015.2020
#-- [YOUR NAME]
#-- [YOUR STUDENT NUMBER] 
#-- [YOUR NAME]
#-- [YOUR STUDENT NUMBER] 


#-- import outside the standard Python library are not allowed, just those:
import math
import numpy
import scipy.spatial
import startin 
#-----

def bbox(point_list, cell_size=1):
    # split the list of 3d points in lists for x and y 
    x_list = []
    y_list = []
    for points in point_list: 
        x = points[0]
        x_list.append(x)
        y = points[1]
        y_list.append(y)
    # find the lower left and upper right coordinate
    min_coordinate = (min(x_list), min(y_list))
    max_coordinate = (max(x_list), max(y_list))

    # find first 
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
    x_axis = []
    y_axis = []
    for i in numpy.arange(min_coordinate[0], max_coordinate[0] + j_nn['cellsize'], j_nn['cellsize']):
        if i <= max_coordinate[0]:
            x_axis.append(i)

    for i in numpy.arange(min_coordinate[1], max_coordinate[1] + j_nn['cellsize'], j_nn['cellsize']):
        if i <= max_coordinate[1]:
            y_axis.append(i)

    grid = numpy.meshgrid(x_axis, y_axis, sparse=True)
    return grid

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
    print("cellsize:", j_nn['cellsize'])

    #-- to speed up the nearest neighbour us a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    # kd = scipy.spatial.KDTree(list_pts)
    # d, i = kd.query(p, k=1)

    print("File written to", j_nn['output-file'])



def idw_interpolation(list_pts_3d, j_idw):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with IDW
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_idw:       the parameters of the input for "idw"
    Output:
        returns the value of the area
 
    """  
    # print("cellsize:", j_idw['cellsize'])
    # print("radius:", j_idw['radius'])

    #-- to speed up the nearest neighbour us a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    # kd = scipy.spatial.KDTree(list_pts)
    # i = kd.query_ball_point(p, radius)
    
    print("File written to", j_idw['output-file'])


def tin_interpolation(list_pts_3d, j_tin):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with linear in TIN interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_tin:       the parameters of the input for "tin"
    Output:
        returns the value of the area
 
    """  
    #-- example to construct the DT with scipy
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html#scipy.spatial.Delaunay
    # dt = scipy.spatial.Delaunay([])

    #-- example to construct the DT with startin
    # minimal docs: https://github.com/hugoledoux/startin_python/blob/master/docs/doc.md
    # how to use it: https://github.com/hugoledoux/startin_python#a-full-simple-example
    # you are *not* allowed to use the function for the tin linear interpolation that I wrote for startin
    # you need to write your own code for this step
    # but you can of course read the code [dt.interpolate_tin_linear(x, y)]
    
    print("File written to", j_tin['output-file'])


def kriging_interpolation(list_pts_3d, j_kriging):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with ordinary kriging interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_kriging:       the parameters of the input for "kriging"
    Output:
        returns the value of the area
 
    """  
    
    
    print("File written to", j_kriging['output-file'])
