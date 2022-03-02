import numpy as np
import matplotlib
#matplotlib.use('Agg')#usefull if no GUI
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

tSNE_values = np.load('tSNE.npy')
elev , azim = 30,-180 + (298)
fig = plt.figure()
ax = plt.axes(projection='3d')
#this is actually usefull
ax.scatter(tSNE_values[417:3642,0],tSNE_values[417:3642,1],tSNE_values[417:3642,2],s=0.2,c='#1D4466', label = 'Population')
ax.scatter(tSNE_values[3643+417:,0],tSNE_values[3643+417:,1],tSNE_values[3643+417:,2],s=.2,c='#EB6934', label = 'Generational')
ax.scatter(tSNE_values[:417,0],tSNE_values[:417,1],tSNE_values[:417,2],s=.2,c='r' ,label='Shared')
#plt.legend()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('tSNE_1' , fontsize=20)
plt.ylabel('tSNE_2' , fontsize=20)
ax.set_zlabel('tSNE_3' , fontsize=20)
plt.tight_layout()
ax.view_init(elev, azim)
plt.show()
#plt.savefig(dpi=300,fname='figure_7.svg')
