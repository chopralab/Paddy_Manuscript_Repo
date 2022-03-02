import torch
import torch.nn as nn
import math, random, sys
import argparse
sys.path.append('icml18-jtnn-master')
from fast_jtnn import *
import rdkit
import paddy
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
	out_mol = Chem.MolFromSmiles(output_b)
	out_FP = Chem.GetMorganFingerprintAsBitVect(out_mol,2,nBits=2**23)
	output_f = Chem.DataStructs.TverskySimilarity(out_FP,target_FP,.5,.01)
	score=output_f
	print(str(output_b)+','+str(start-time.time())+', fitness:'+str(score))
	return -score

start = time.time()
best = fmin(fn=run_func_1, space=fspace, algo=tpe.suggest, max_evals=3500,rstate=np.random.RandomState(seed))
end  = time.time()
print("run time:"+str(end-start))




