import torch
import ast
import argparse
import os
import time
import random
import numpy as np
import networkx as nx
import rdkit
from rdkit.Chem import AllChem as Chem
from rdkit.Chem import MolFromSmiles, MolToSmiles, Descriptors, DataStructs
import sys
# Go back two directories and append to the system path
#os.chdir('../../')  This doesn't work?
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from icml18_jtnn_master.fast_jtnn import *
from icml18_jtnn_master.fast_jtnn import Vocab
from icml18_jtnn_master.fast_jtnn import JTNNVAE
import json
import warnings

# Filter out the specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn._reduction")
warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.functional")

# Setting random seeds and environment variables for reproducibility and GPU usage
random.seed(2)
np.random.seed(8)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Suppressing logging from rdkit library
logger = rdkit.RDLogger.logger()
logger.setLevel(rdkit.RDLogger.CRITICAL)


# Loading vocabulary from file and initializing Vocab object
vocab_file_path = 'vocab.txt'
vocab = [x.strip("\r\n ") for x in open(vocab_file_path)]
vocab = Vocab(vocab)

# Initializing and loading a pre-trained model
model = JTNNVAE(vocab, 450, 56, 20, 3)
pretrained_model_path = 'model.iter-400000'
model.load_state_dict(torch.load(pretrained_model_path))
model = model.cuda()

# Initialize an argument parser
parser = argparse.ArgumentParser()

# Add argument to the parser for 'Vector' which is expected to be a string
# Add argument to the parser for 'OUTPUT'. It defaults to 'vol/output.txt' if not specified
parser.add_argument('--Vector', type=str, required=True)
parser.add_argument('--OUTPUT', type=str, default='vol/smiles_out.txt')
# Parse the arguments and assign it to the args variable
args = parser.parse_args()

Vector = args.Vector.replace('\n', '')
if len(ast.literal_eval(Vector)) != 56:
    raise ValueError('Length of vector must be 56, receieved len {}'.format(len(ast.literal_eval(Vector))))
Vector = torch.tensor(ast.literal_eval(Vector))
output = args.OUTPUT


encoded_data_part1 = torch.randn(1, 28).cuda()
encoded_data_part2 = torch.randn(1, 28).cuda()


# Setting values for encoded_data_part1 and encoded_data_part2 from input_values
for idx, value in enumerate(Vector[:28]):
    encoded_data_part1[0][idx] = value.item()
for idx, value in enumerate(Vector[28:]):
    encoded_data_part2[0][idx] = value.item()




# Decoding to SMILES string and converting to molecule

decoded_smiles = model.decode(encoded_data_part1, encoded_data_part2, False)

print('JTVAE has finished processing')
print('Molecule selected')
print(json.dumps({'smiles':decoded_smiles}, indent=2))

with open(output, 'w') as f:
    f.write(json.dumps({'smiles':decoded_smiles}, indent=2))

f.close()
