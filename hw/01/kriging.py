import math
import numpy
import scipy.spatial
import startin 

import sys
import csv
import json

#-- read the needed parameters from the file 'params.json' (must be in same folder)
try:
    jparams = json.load(open('params.json'))
except:
    print("ERROR: something is wrong with the params.json file.")
    sys.exit()
#-- store the input 3D points in list
list_pts_3d = []
with open(jparams['input-file']) as csvfile:
    j_krig = jparams['kriging']
    r = csv.reader(csvfile, delimiter=' ')
    header = next(r)
    for line in r:
        p = list(map(float, line)) #-- convert each str to a float
        assert(len(p) == 3)
        list_pts_3d.append(p)

cellsize= j_krig['cellsize']
radius = j_krig['radius']


