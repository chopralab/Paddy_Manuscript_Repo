import os
import time
import torch
import random
import numpy as np
import networkx as nx
import rdkit
from rdkit.Chem import AllChem as Chem
from rdkit.Chem import MolFromSmiles, MolToSmiles, Descriptors, DataStructs
import sys
sys.path.append('/home/sanjay/Paddy_Manuscript_Repo')
from icml18_jtnn_master.fast_jtnn import *
from icml18_jtnn_master.fast_jtnn import Vocab
from icml18_jtnn_master.fast_jtnn import JTNNVAE

# Setting random seeds and environment variables for reproducibility and GPU usage
random.seed(2)
np.random.seed(8)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Suppressing logging from rdkit library
logger = rdkit.RDLogger.logger()
logger.setLevel(rdkit.RDLogger.CRITICAL)

print('os_getcwd', os.getcwd())
# Loading vocabulary from file and initializing Vocab object
vocab_file_path = '/home/sanjay/Paddy_Manuscript_Repo/icml18_jtnn_master/fast_molvae/vocab.txt'
vocab = [x.strip("\r\n ") for x in open(vocab_file_path)]
vocab = Vocab(vocab)

# Initializing and loading a pre-trained model
model = JTNNVAE(vocab, 450, 56, 20, 3)
base_directory = '/home/sanjay/Paddy_Manuscript_Repo/'
pretrained_model_path = os.path.join(base_directory, 'icml18_jtnn_master/fast_molvae/moses-h450z56/model.iter-400000')
model.load_state_dict(torch.load(pretrained_model_path))
model = model.cuda()

#Old search space
# # Defining the search space for the optimization algorithm
# search_space = paddy.Default_Numerics.Polynomial(length=56, scope=1, gaussian_type='scaled', normalization=True, limits=[-1, 1])

#New search space
#torch.rand(56) creates a tensor of size 56 with values in [0, 1).
#  When you multiply this tensor by 2, the values are now in the range [0, 2). 
# Finally, when you subtract 1 from these values, they are shifted into the range [-1, 1).
initial_solution = torch.rand(56) * 2 - 1



# Defining the target molecule and computing its fingerprint
target_smiles = 'O=S(=O)(N)c1c(ccc(c1)Nc2nccc(n2)N(c4ccc3c(nn(c3C)C)c4)C)C'
target_molecule = Chem.MolFromSmiles(target_smiles)
target_fingerprint = Chem.GetMorganFingerprintAsBitVect(target_molecule, 2, nBits=2**23)

def evaluate_similarity(input_values):
    encoded_data_part1 = torch.randn(1, 28).cuda()
    encoded_data_part2 = torch.randn(1, 28).cuda()
    
    # Setting values for encoded_data_part1 and encoded_data_part2 from input_values
    for idx, value in enumerate(input_values[:28]):
        encoded_data_part1[0][idx] = value[0]
    for idx, value in enumerate(input_values[28:]):
        encoded_data_part2[0][idx] = value[0]
    
    # Decoding to SMILES string and converting to molecule
    decoded_smiles = model.decode(encoded_data_part1, encoded_data_part2, False)
    decoded_molecule = Chem.MolFromSmiles(decoded_smiles)
    
    # Computing fingerprint and similarity score
    decoded_fingerprint = Chem.GetMorganFingerprintAsBitVect(decoded_molecule, 2, nBits=2**23)
    #similarity_score = Chem.DataStructs.TverskySimilarity(decoded_fingerprint, target_fingerprint, 0.5, 0.01)
    
    # Writing results to file
    with open('JTVAE_results.txt', 'a') as file:
        file.write("{}, fitness: {}\n".format(decoded_smiles))

    # Printing results to console
    print("{}, fitness: {}".format(decoded_smiles))

    
    # Returning similarity score
    #return similarity_score



# # Initializing the optimization algorithm
# optimizer = paddy.PFARunner(space=search_space, eval_func=evaluate_similarity, rand_seed_number=250, yt=15, paddy_type='generational', Qmax=25, r=5, iterations=30)

# # Running the optimization algorithm
# start_time = time.time()
# optimizer.run_paddy()
# end_time = time.time()

# # Saving the results
# optimizer.save_paddy('Paddy_Tversky_Gen')

# # Printing total runtime
# print(f"Total runtime: {end_time - start_time} seconds")