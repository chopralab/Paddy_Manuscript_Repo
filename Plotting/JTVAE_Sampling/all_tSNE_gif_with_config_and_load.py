import numpy as np
import matplotlib
matplotlib.use('Agg')
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#This can be used to generate the needed npy file bellow 
#ppvf=np.load('all_paddy.npy')#pop then gen seed values
#tsne = TSNE(n_components=3, verbose=1, perplexity=40, n_iter=300)
#t15 = tsne.fit_transform(ppvf)
#np.save('tsne_all',t15)

t15 = np.load('tsne_all.npy')
#file = open(r"gif/config2.txt","w")	
elev , azim = 30,-180
for i in range(0,370,2):
	fig = plt.figure()
	ax = plt.axes(projection='3d')
	#this is actually usefull
	ax.scatter(t15[417:3642,0],t15[417:3642,1],t15[417:3642,2],s=0.2,c='#1D4466', label = 'Population')
	ax.scatter(t15[3643+417:,0],t15[3643+417:,1],t15[3643+417:,2],s=.2,c='#EB6934', label = 'Generational')
	ax.scatter(t15[:417,0],t15[:417,1],t15[:417,2],s=.2,c='r' ,label='Shared')
	#plt.legend()
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.xlabel('tSNE_1' , fontsize=20)
	plt.ylabel('tSNE_2' , fontsize=20)
	ax.set_zlabel('tSNE_3' , fontsize=20)
	plt.tight_layout()
	#plt.savefig(dpi=300,fname='tSNE.svg')
	ax.view_init(elev, azim+i)
	plt.savefig(dpi=300,fname='gif/tSNE_3D_{0}.jpg'.format(i))
	#file.write('gif/tSNE_3D_{0}.jpg\n'.format(i))
	plt.show()
	plt.close()

#file.close()

'''
#single frame svg
t15 = np.load('tsne_all.npy')
elev , azim = 30,-180 + (298)
fig = plt.figure()
ax = plt.axes(projection='3d')
#this is actually usefull
ax.scatter(t15[417:3642,0],t15[417:3642,1],t15[417:3642,2],s=0.2,c='#1D4466', label = 'Population')
ax.scatter(t15[3643+417:,0],t15[3643+417:,1],t15[3643+417:,2],s=.2,c='#EB6934', label = 'Generational')
ax.scatter(t15[:417,0],t15[:417,1],t15[:417,2],s=.2,c='r' ,label='Shared')
#plt.legend()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('tSNE_1' , fontsize=20)
plt.ylabel('tSNE_2' , fontsize=20)
ax.set_zlabel('tSNE_3' , fontsize=20)
plt.tight_layout()
ax.view_init(elev, azim)
plt.savefig(dpi=300,fname='tSNE_3D.svg')
'''
