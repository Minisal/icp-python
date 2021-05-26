import matplotlib.pyplot as plt 
from plyfile import *
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plydata = PlyData.read("bun045.ply")
plydata2 = PlyData.read("bun000.ply")

xlist = plydata['vertex']['x']
ylist = plydata['vertex']['y']
zlist = plydata['vertex']['z']

xlist2 = plydata2['vertex']['x']
ylist2 = plydata2['vertex']['y']
zlist2 = plydata2['vertex']['z']


fig = plt.figure()
ax = Axes3D(fig)
# ax.scatter(xlist,ylist,zlist)
# ax.bar3d(xlist,ylist,zlist,dx,dy,dz,color="red")
ax.scatter(xlist,ylist,zlist,c="red")
ax.scatter(xlist2,ylist2,zlist2,c="blue")
ax.azim=-90
ax.dist=10
ax.elev=90

plt.show()