###Surface plot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import math



def function_2(x,y):
    r1=((x-0.5)**2)+((y-0.5)**2)
    r2=((x-0.6)**2)+((y-0.1)**2)
    result = (0.80*math.exp(-(r1)/(0.3**2))) + (0.88*math.exp(-(r2)/0.03**2))
    #global maximum at (0.6,0.1) with local at (0.5,0.5)
    return (result)


X = np.arange(0, 1, 0.01)
Y = np.arange(0, 1, 0.01)
X, Y = np.meshgrid(X, Y)

Z = np.empty([100,100])

c = 0
for i in Z:
	c2 = 0
	for i2 in i:
		Z[c][c2] = function_2(X[c][c2],Y[c][c2])
		c2 += 1
	c += 1

r_list = np.load('hp_minmax.npy')

xs=[]
ys=[]
zs=[]
for i in b_list:
	xs.append(i[0]['x'])
	ys.append(i[0]['y'])
	zs.append(-i[1])

r_list = np.load('paddy_minmax.npy')

xs2=[]
ys2=[]
zs2=[]
for i in r_list:
	xs2.append(i[0][0][0])
	ys2.append(i[0][1][0])
	zs2.append(i[1])


fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

pos = ax.scatter(xs,ys,zs,c='k')

plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap=cm.summer)
pos = ax.scatter(xs,ys,zs,s=5,c='#8ac6d1ff',edgecolors='#1f77b4ff')
ax.set_zlabel('z',fontsize=18)
ax.set_xlabel('x',fontsize=18)
ax.set_ylabel('y',fontsize=18)
ax.zaxis.set_tick_params(labelsize=14,size=15)
ax.xaxis.set_tick_params(labelsize=15,size=15)
ax.yaxis.set_tick_params(labelsize=14,size=15)
ax.set_title('Hyperopt',fontsize=15)
#plt.savefig(filename='hpf2.svg',dpi=300)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap=cm.summer)
pos = ax.scatter(xs2,ys2,zs2,s=2,c='#8ac6d1ff',edgecolors='#1f77b4ff')
ax.set_zlabel('z',fontsize=18)
ax.set_xlabel('x',fontsize=18)
ax.set_ylabel('y',fontsize=18)
ax.zaxis.set_tick_params(labelsize=14,size=15)
ax.xaxis.set_tick_params(labelsize=15,size=15)
ax.yaxis.set_tick_params(labelsize=14,size=15)
ax.set_title('Paddy',fontsize=15)
#plt.savefig(filename='paddyf2.svg',dpi=300)
plt.show()

