import torch
import torch.nn as nn
import math, random, sys
import argparse
from fast_jtnn import *
import rdkit
import paddy
from rdkit.Chem import AllChem as Chem
import time
import numpy as np
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
   
vocab = [x.strip("\r\n ") for x in open('vocab.txt')] 
vocab = Vocab(vocab)

model = JTNNVAE(vocab, 450, 56, 20, 3)
model.load_state_dict(torch.load('moses-h450z56/model.iter-400000'))
model = model.cuda()

space = paddy.Default_Numerics.Polynomial(length=56, scope=1, gausian_type='scaled',normalization=True, limits=[-1,1])

target_mol = Chem.MolFromSmiles('O=S(=O)(N)c1c(ccc(c1)Nc2nccc(n2)N(c4ccc3c(nn(c3C)C)c4)C)C')
target_FP = Chem.GetMorganFingerprintAsBitVect(target_mol,2,nBits=2**23)



def run_func_1(input):
	input = input
	ar1 = torch.randn(1, 28).cuda()
	ar2 = torch.randn(1, 28).cuda()
	c = 0
	for i in input[0:28]:
		ar1[0][c] = i[0]
		c += 1
	c = 0
	for i in input[28:]:
		ar2[0][c] = i[0]
		c +=1
	output_b = model.decode(ar1,ar2,False)
	out_mol = Chem.MolFromSmiles(output_b)
	out_FP = Chem.GetMorganFingerprintAsBitVect(out_mol,2,nBits=2**23)
	output_f = Chem.DataStructs.TverskySimilarity(out_FP,target_FP,.5,.01)
	score=(output_f)
	print(str(output_b)+','+str(start-time.time())+', fitness:'+str(score))
	return score


runner = paddy.PFARunner(space=space, eval_func=run_func_1, rand_seed_number = 250, yt = 15, paddy_type='population', Qmax=25, r=5, iterations=30)
start = time.time()
runner.run_paddy()
end = time.time()
runner.save_paddy('Pady_Tversky_Pop')
print("run time:"+str(end-start))
