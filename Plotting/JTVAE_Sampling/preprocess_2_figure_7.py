import numpy as np
import sklearn
from sklearn.manifold import TSNE

#This can be used to generate the needed npy file bellow 
paddy_values=np.load('All_Paddy.npy')#pop then gen seed values
tsne = TSNE(n_components=3, verbose=1, perplexity=40, n_iter=300)
tSNE_values = tsne.fit_transform(paddy_values)
np.save('tSNE',tSNE_values)
