import numpy as np
import matplotlib
matplotlib.use('Agg')
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

t15 = np.load('umap_all.npy')
#file = open(r"gif/config2.txt","w")	
elev , azim = 30,-180
for i in range(0,370,2):
	fig = plt.figure()
	ax = plt.axes(projection='3d')
	#this is actually usefull
	ax.scatter(t15[417:3642,0],t15[417:3642,1],t15[417:3642,2],s=0.2,c='#89D0D3', label = 'Population')
	ax.scatter(t15[3643+417:,0],t15[3643+417:,1],t15[3643+417:,2],s=.2,c='#DF8F9F', label = 'Generational')
	ax.scatter(t15[:417,0],t15[:417,1],t15[:417,2],s=.2,c='#A186E7' ,label='Shared')
	#plt.legend()
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.xlabel('Component_1' , fontsize=20)
	plt.ylabel('Component_2' , fontsize=20)
	ax.set_zlabel('Component_3' , fontsize=20)
	plt.tight_layout()
	#plt.savefig(dpi=300,fname='tSNE.svg')
	ax.view_init(elev, azim+i)
	plt.savefig(dpi=300,fname='gif/umap_3D_{0}.jpg'.format(i))
	plt.show()
	plt.close()


