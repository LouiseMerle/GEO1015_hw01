import math

cellsize = 3.0
x_list_points = [8, 2]
x_list_points = [8.8, 2.3]

ncols1 = math.ceil((max(x_list_points)-min(x_list_points))/cellsize)
ncols = math.ceil((max(x_list_points)-min(x_list_points) + (0.5 * cellsize))/cellsize)
print(ncols1)
print(ncols)

range_x1 = range(int(min(x_list_points)), int(ncols * cellsize + cellsize), int(cellsize))

range_x = range(int(min(x_list_points)), int(max(x_list_points) + cellsize), int(cellsize))

print(range_x1)
print(range_x)

    