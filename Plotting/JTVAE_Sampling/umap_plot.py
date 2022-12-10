import numpy as np
import matplotlib
matplotlib.use('Agg')#usefull if no GUI
import umap
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random 

seed = 7
np.random.seed(seed)
random.seed(1)

paddy_values = np.load('All_Paddy.npy')
mapper = umap.UMAP(n_components=3,n_neighbors=15,min_dist=0.5).fit(paddy_values)
umap_values = mapper.fit_transform(paddy_values)
np.save('umap_all',umap_values)
elev , azim = 30,-180 + (298)
fig = plt.figure()
ax = plt.axes(projection='3d')
#this is actually usefull
ax.scatter(umap_values[417:3642,0],umap_values[417:3642,1],umap_values[417:3642,2],s=0.2,c='#89D0D3', label = 'Population')
ax.scatter(umap_values[3643+417:,0],umap_values[3643+417:,1],umap_values[3643+417:,2],s=0.2,c='#DF8F9F', label = 'Generational')
ax.scatter(umap_values[:417,0],umap_values[:417,1],umap_values[:417,2],s=0.2,c='#A186E7' ,label='Shared')
leg = plt.legend(markerscale=10, fontsize = 12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Component_1' , fontsize=20)
plt.ylabel('Component_2' , fontsize=20)
ax.set_zlabel('component_3' , fontsize=20)
plt.tight_layout()
ax.view_init(elev, azim)
plt.show()
plt.savefig(dpi=300,fname='umap.pdf')
