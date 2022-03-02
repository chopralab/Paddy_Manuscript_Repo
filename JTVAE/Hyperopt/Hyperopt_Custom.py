import torch
import torch.nn as nn
import math, random, sys
import argparse
sys.path.append('icml18-jtnn-master')
from fast_jtnn import *
import rdkit
from rdkit.Chem import AllChem as Chem
import hyperopt
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import time
import numpy as np
sys.path.append('icml18-jtnn-master/bo')
import sascorer
import networkx as nx
from rdkit.Chem import rdmolops
from rdkit.Chem import MolFromSmiles, MolToSmiles
from rdkit.Chem import Descriptors
import os

random.seed(2)
seed = 8
np.random.seed(seed)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

lg = rdkit.RDLogger.logger() 
lg.setLevel(rdkit.RDLogger.CRITICAL)
   
vocab = [x.strip("\r\n ") for x in open('icml18-jtnn-master/fast_molvae/vocab.txt')] 
vocab = Vocab(vocab)

model = JTNNVAE(vocab, 450, 56, 20, 3)
model.load_state_dict(torch.load('icml18-jtnn-master/fast_molvae/moses-h450z56/model.iter-400000'))
model = model.cuda()


target_mol = Chem.MolFromSmiles('O=S(=O)(N)c1c(ccc(c1)Nc2nccc(n2)N(c4ccc3c(nn(c3C)C)c4)C)C')
target_FP = Chem.GetMorganFingerprintAsBitVect(target_mol,2,nBits=2**23)



def pspace_maker(leng):
    c = 0
    pspace = {}
    while c < leng:
        pspace['x{0}'.format(c)]= hp.uniform('x{0}'.format(c),-1,1)
        c += 1
    return (pspace)

fspace = pspace_maker(56)


def scorer(mol):
        cycle_list = nx.cycle_basis(nx.Graph(rdmolops.GetAdjacencyMatrix(mol)))
        if len(cycle_list) == 0:
            cycle_length = 0
        else:
            cycle_length = max([ len(j) for j in cycle_list ])
        if cycle_length <= 6:
            cycle_length = 0
        else:
            cycle_length = cycle_length - 6
        current_cycle_score = -cycle_length
        if len(cycle_list) > 2:
            if len(cycle_list)<6:
                cycle_count = 0
            else:
                cycle_count = abs(len(cycle_list)-5)
        else:
            cycle_count = abs(len(cycle_list)-2)
        #score = (-sascorer.calculateScore(MolFromSmiles(smile)) + Descriptors.MolLogP(MolFromSmiles(smile)) + current_cycle_score)
        score = (sascorer.calculateScore(mol)**-1  + current_cycle_score)
        return(score,cycle_count)


def run_func_1(input):
	input = input
	ar1 = torch.randn(1, 28).cuda()
	ar2 = torch.randn(1, 28).cuda()
	c = 0
	while c < 28:
		ar1[0][c] = input['x{0}'.format(c)]
		c += 1
	c = 0
	while c < 28:
		ar2[0][c] = input['x{0}'.format(c+28)]
		c += 1
	output_b = model.decode(ar1,ar2,False)
	if output_b != 'kill me':
		out_mol = Chem.MolFromSmiles(output_b)
		out_FP = Chem.GetMorganFingerprintAsBitVect(out_mol,2,nBits=2**23)
		output_f = Chem.DataStructs.TverskySimilarity(out_FP,target_FP,.5,.01)
		output_f2,cycle_count = scorer(out_mol)
		rb=(rdkit.Chem.QED.properties(out_mol)[-3])
		bo = (out_FP.GetNumOnBits()) -45
		bos = 1
		if bo < 0:
			bos = 0.6**abs(bo)
		if rb > 2:
		    if rb<7:
		        rbs = 0
		    else:
		        rbs = rb-5
		else:
		    rbs = 2-rb
		print(str(output_b)+','+str(start-time.time())+', fitness:'+str((output_f*rdkit.Chem.Descriptors.FpDensityMorgan3(out_mol)**2)*(.1**rbs)*bos*output_f2*.1**cycle_count))
		return -(output_f*rdkit.Chem.Descriptors.FpDensityMorgan3(out_mol)**2)*(.1**rbs)*bos*output_f2*.1**cycle_count
	else:
		score = 1
	print(str(output_b)+','+str(start-time.time())+', fitness:'+str(score))
	return -score

start = time.time()
best = fmin(fn=run_func_1, space=fspace, algo=tpe.suggest, max_evals=3500,rstate=np.random.RandomState(seed))
end  = time.time()
print("run time:"+str(end-start))




