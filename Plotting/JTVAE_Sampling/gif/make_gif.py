import imageio
images = []
for i in range(0,370,2):
	images.append(imageio.imread('umap_3D_{0}.jpg'.format(i)))
imageio.mimsave('../umap.gif', images)
