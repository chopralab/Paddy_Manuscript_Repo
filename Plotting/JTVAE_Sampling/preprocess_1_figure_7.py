import numpy as np
import paddy
import sklearn

def run_func_1():#dummy function for paddy loading
	pass

paddy_run = paddy.utils.paddy_recover('Paddy_Custom_Pop')#paddy_vae_pop_custom.pickle
paddy_run2 = paddy.utils.paddy_recover('Paddy_Custom_Gen')#paddy_vae_gen_custom.pickle

vals2 = []
for i in paddy_run.seed_params:
	vals2.append(i[:,0])

for i in paddy_run2.seed_params:
	vals2.append(i)

np.save('all_paddy',vals2)
