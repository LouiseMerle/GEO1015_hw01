#-- my_code_hw01.py
#-- hw01 GEO1015.2020
#-- Carolin Bachert
#-- 5382998
#-- Louise Spekking
#-- 4256778  


#-- import outside the standard Python library are not allowed, just those:
import math
import numpy
import scipy.spatial
import startin 
#-----

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

# function to calculate the new height value at an unknown location
def cellvalue_idw(raster_point, r, p, kd_tree, zip_list, z_list_points):               
    # raster point is centerpoint of cell
        
        # i_idw list of indicies with points within radius
        i_idw = kd_tree.query_ball_point(raster_point, r)       

        # Assign no Data value if there is no sample point within radius
        if len(i_idw) == 0:
            return -9999

        # calculate the weight that is assigned to each sample point within the search radius
        weight_list = []
        for i in i_idw:
            if distance(zip_list[i], raster_point) == 0:
                z_value = z_list_points[i]
                return z_value
            else:
                d = distance(raster_point, zip_list[i])
                w_i = 1/d ** p
                weight_list.append(w_i)
        
        # create a list with the height values of the sample points within the search radius
        point_list = []
        for i in i_idw:
            point_list.append(z_list_points[i])

        # get the value of the counter for the formula to calculate the new height value
        s = 0
        for num1, num2 in zip(weight_list, point_list):
            s += num1 * num2

        # returns the new height value
        return(s/sum(weight_list))

# function to remove dubble points in sample and return array of points (taken from variogram.py) 
def remove_doubles(points_list):
    clean_points_list = []
    for point1 in points_list:
        repeated = False
        for point2 in clean_points_list:
            if point1[0] == point2[0] and point1[1] == point2[1]:
                repeated = True
        if repeated == False:
            clean_points_list.append(point1)
    return numpy.array(clean_points_list)

# gaussian equation 
def gaussian(nugget, still, range_kriging, distance_sample_raster):
    exponent = (-(3 * distance_sample_raster)**2) / (range_kriging ** 2) 
    result = still * (1 - math.e ** exponent) + nugget
    return result

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

    # get cellsize from j_params file 
    cellsize = j_nn['cellsize']
   
    # split the list of 3d sample points in lists for x, y and z 
    x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)

    # create the KDTree with the x and y values of the sample points 
    xy_list = list(zip(x_list_points, y_list_points))
    tree = scipy.spatial.KDTree(xy_list) 

    # calcalute number of rows and colums to wtrite in the asc file
    ncols = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
    nrows = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
    
    # make x and y ranges for the x and y axes for the bbox
    # add 0.5 cellsize to find the centre points of the cell
    # reverse y write in asc file from top to bottom 
    range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
    range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)
    
    # make list with all x y coordinates on the x and y axis of the raster
    coordinate_lst = [[x, y] for y in range_y for x in range_x]
    
    # convex hull
    hull = scipy.spatial.Delaunay(xy_list)

    # query the raster coordinates with the sample points 
    # append interpolated z value to list with x, y raster coordinates
    # assign no Data value if cell center is outside convex hull 
    for query_point in coordinate_lst:
        if hull.find_simplex(query_point) == -1:
            query_point.append(-9999)
        else:
            d, i_nn = tree.query(query_point,k=1)
            query_point.append(z_list_points[i_nn])

    # count row and column numbers to write row by row in asc file 
    row_nr = 0
    col_nr = 0

    # open asc output file and write 
    with open(j_nn['output-file'], 'w') as fh:
        fh.write('NCOLS {}\n'.format(ncols))
        fh.write('NROWS {}\n'.format(nrows))
        fh.write('XLLCENTER {}\n'.format(min(x_list_points) + (0.5 * cellsize)))
        fh.write('YLLCENTER {}\n'.format(min(y_list_points) + (0.5 * cellsize)))
        fh.write('CELLSIZE {}\n'.format(j_nn['cellsize']))
        fh.write('NODATA_VALUE {}\n'.format(-9999))
        
        # write z values in asc file 
        for point in coordinate_lst:
            fh.write(str(point[-1])+' ')
            col_nr += 1
        
            # print new line charater when nr of colls is reached and row is full
            if col_nr == ncols:
                col_nr = 0
                row_nr += 1
                fh.write('\n')

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

    # get cellsize, radius and power from j_params file
    cellsize= j_idw['cellsize']
    radius = j_idw['radius']
    power = j_idw['power']

    # split the list of 3d sample points in lists for x, y and z 
    x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)
    
    # create the KDTree with the x and y values of the sample points
    xy_list = list(zip(x_list_points, y_list_points))
    tree = scipy.spatial.KDTree(xy_list)

    # calcalute number of rows and colums to wtrite in the asc file
    ncols = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
    nrows = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
    
    # make x and y ranges for the x and y axes for the bbox
    # add 0.5 cellsize to find the centre points of the cell
    # reverse y write in asc file from top to bottom 
    range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
    range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)
    
    # make list with all x y coordinates on the x and y axis of the raster
    coordinate_lst = [[x, y] for y in range_y for x in range_x]

    # convex hull
    hull = scipy.spatial.Delaunay(xy_list)

    # query the raster coordinates with the above function cellvalue_idw  
    # append interpolated z value to list with x, y raster coordinates
    # assign no Data value if cell center is outside convex hull
    for point in coordinate_lst:
        if hull.find_simplex(point) == -1:
            point.append(-9999)
        else:
            point.append(cellvalue_idw(point, radius, power, tree, xy_list, z_list_points))

    # count row and column numbers to write row by row in asc file     
    row_nr = 0
    col_nr = 0

    # open asc output file and write
    with open(j_idw['output-file'], 'w') as fh:
        fh.writelines('NCOLS {}\n'.format(ncols))
        fh.writelines('NROWS {}\n'.format(nrows))
        fh.writelines('XLLCENTER {}\n'.format(min(x_list_points) + (0.5 * cellsize)))
        fh.writelines('YLLCENTER {}\n'.format(min(y_list_points) + (0.5 * cellsize)))
        fh.writelines('CELLSIZE {}\n'.format(j_idw['cellsize']))
        fh.writelines('NODATA_VALUE {}\n'.format(-9999))
        
        # write z values in asc file
        for point in coordinate_lst:
            fh.write(str(point[-1])+' ')
            col_nr += 1

            # print new line charater when nr of colls is reached and row is full
            if col_nr == ncols:
                col_nr = 0
                row_nr += 1
                fh.write('\n')

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
    cellsize = j_tin['cellsize']
   
    # split the list of 3d sample points in lists for x, y and z 
    x_list_points, y_list_points, z_list_points = split_xyz(list_pts_3d)

    # create list with x and y values of 3d points list 
    xy_list = list(zip(x_list_points, y_list_points))

    # calcalute number of rows and colums to wtrite in the asc file
    ncols = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
    nrows = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
    
    # make x and y ranges for the x and y axes for the bbox
    # add 0.5 cellsize to find the centre points of the cell
    # reverse y write in asc file from top to bottom 
    range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
    range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)
    
    # make list with all x y coordinates on the x and y axis of the raster
    coordinate_lst = [[x, y] for y in range_y for x in range_x]
    
    # convex hull
    # used for triangulation
    hull = scipy.spatial.Delaunay(xy_list)
    
    # find simplex rasterpoint falls in
    for raster_point in coordinate_lst:
        simplex = hull.find_simplex(raster_point)
        # find vertices of simplex
        vertices = hull.vertices[simplex]

        # is not in convex hull, assing no data value
        if simplex == -1:
            raster_point.append(-9999)
        else: 
            # find point on raster with index of vertices
            p1 = xy_list[vertices[0]]
            p2 = xy_list[vertices[1]]
            p3 = xy_list[vertices[2]]

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
                # use barycentric coordinates
                w1 = ((p2[1] - p3[1]) * (raster_point[0] - p3[0]) + (p3[0] - p2[0]) * (raster_point[1] - p3[1])) / ((p2[1] - p3[1]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[1] - p3[1]))
                w2 = ((p3[1] - p1[1]) * (raster_point[0] - p3[0]) + (p1[0] - p3[0]) * (raster_point[1] - p3[1])) / ((p2[1] - p3[1]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[1] - p3[1]))
                w3 = 1 - w1 - w2

            # calculate z value 
            z_value = (w1 * z_list_points[vertices[0]] + w2 * z_list_points[vertices[1]] + w3 * z_list_points[vertices[2]]) / (w1 + w2 + w3)

            # append z value to raster point coordinates
            raster_point.append(z_value)

    # count row and column numbers to write row by row in asc file 
    row_nr = 0
    col_nr = 0

    # open asc output file and write 
    with open(j_tin['output-file'], 'w') as fh:
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
    # get cellsize and search radius 
    cellsize= j_kriging['cellsize']
    radius = j_kriging['radius']

    # set variables as found by variogram
    nugget = 0
    still = 1400
    range_kriging = 300

    #remove all double points from point list
    points_3d_array = remove_doubles(list_pts_3d)

    # split the list of 3d sample points in lists for x, y and z 
    x_list_points, y_list_points, z_list_points = split_xyz(points_3d_array)

    # create the KDTree with the x and y values of the sample points 
    xy_list = list(zip(x_list_points, y_list_points))
    tree = scipy.spatial.KDTree(xy_list) 

    # calcalute number of rows and colums to wtrite in the asc file
    ncols = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
    nrows = math.ceil((max(y_list_points)-min(y_list_points))/cellsize)
        
    # make x and y ranges for the x and y axes for the bbox
    # add 0.5 cellsize to find the centre points of the
    # reverse y write in asc file from top to bottom 
    range_y = reversed(numpy.arange(min(y_list_points) + 0.5 * cellsize, max(y_list_points)+ 0.5 * cellsize, cellsize)) 
    range_x = numpy.arange(min(x_list_points) + 0.5 * cellsize, max(x_list_points)+ 0.5 * cellsize, cellsize)
        
    # make list with all x y coordinates on the x and y axis of the raster
    coordinate_lst = [[x, y] for y in range_y for x in range_x]
        
    # convex hull
    hull = scipy.spatial.Delaunay(xy_list)

    # loop over raster points 
    for raster_point in coordinate_lst:
        # if not in convex hull, assing no data value
        if hull.find_simplex(raster_point) == -1:
            raster_point.append(-9999)
        
        # find points in radius 
        else:
            i_krig = tree.query_ball_point(raster_point, radius)
            # if no values in search radius append no data value as z value to point 
            if len(i_krig) == 0:
                raster_point.append(-9999)
            
            else:
                d = []
                # creat matrix A to fill 
                A = numpy.ones((len(i_krig)+1, len(i_krig)+1))
                # fill lower right value of matrix with 0
                A[len(i_krig)][len(i_krig)] = 0
                row_nr = 0
                col_nr = 0 
                for point_index in i_krig:
                    # if sample point is on a raster point assign hight value of raster point
                    #if distance(xy_list[point_index], raster_point) == 0:
                      #  z_value = z_list_points[point_index]
                      #  raster_point.append(z_value)
                       # print('point on raster point')
                      #  A = []
                      #  d = []
                      #  break
                    #else: 
                    # find values for vector d
                    raster_sample_dist = distance(raster_point, xy_list[point_index])
                    gamma = gaussian(nugget, still, range_kriging, raster_sample_dist)
                    d.append(gamma)
                    # find values for matrix A
                    for other_point_index in i_krig:
                        dist = distance(xy_list[point_index], xy_list[other_point_index])
                        gamma = gaussian(nugget, still, range_kriging, dist)
                        A[row_nr][col_nr] = gamma
                        col_nr += 1 
                        # check if end of column is reached, set writing to next line
                        if col_nr == len(i_krig):
                            row_nr += 1
                            col_nr = 0
                if len(d) > 0:
                    # append 1 to end of vector D 
                    d.append(1)
                    # cast to numpy array 
                    d_vector = numpy.array(d)

                # inverse matrix A 
                A_inverse = numpy.linalg.inv(A)

                # compute weights vector 
                w = numpy.dot(A_inverse,d)
                # remove last element of the weights vector as this is μ(x0)
                weights_vector = w[:-1]

                weight_index_lst = list(zip(weights_vector, i_krig))
                z_value = 0
                # calculate z value with weights 
                for weight, index in weight_index_lst:
                    z_point = z_list_points[index] 
                    z_value += z_point * weight

                # check if compute z value us realistic
                if z_value >= min(z_list_points) and z_value <= max(z_list_points):
                    raster_point.append(z_value)
                # if z value lower than lowest z vlaue in the data set or higher than the highest z vlaue of the data set zet no data value 
                else: 
                    raster_point.append(-9999)
    # count row and column numbers to write row by row in asc file 
    row_nr = 0
    col_nr = 0

    # open asc output file and write 
    with open(j_kriging['output-file'], 'w') as fh:
        fh.write('NCOLS {}\n'.format(ncols))
        fh.write('NROWS {}\n'.format(nrows))
        fh.write('XLLCENTER {}\n'.format(min(x_list_points) + (0.5 * cellsize)))
        fh.write('YLLCENTER {}\n'.format(min(y_list_points) + (0.5 * cellsize)))
        fh.write('CELLSIZE {}\n'.format(j_kriging['cellsize']))
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
        
        print("File written to", j_kriging['output-file'])
