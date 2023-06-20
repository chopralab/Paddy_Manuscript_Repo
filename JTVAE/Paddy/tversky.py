import os
import time
import torch
import random
import numpy as np
import networkx as nx
import rdkit
from rdkit.Chem import AllChem as Chem
from rdkit.Chem import MolFromSmiles, MolToSmiles, Descriptors, DataStructs
from icml18_jtnn_master.fast_jtnn import *


# Setting random seeds and environment variables for reproducibility and GPU usage
random.seed(2)
np.random.seed(8)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Suppressing logging from rdkit library
logger = rdkit.RDLogger.logger()
logger.setLevel(rdkit.RDLogger.CRITICAL)

# Loading vocabulary from file and initializing Vocab object
vocab_file_path = 'icml18-jtnn-master/fast_molvae/vocab.txt'
vocab = [x.strip("\r\n ") for x in open(vocab_file_path)]
vocab = Vocab(vocab)

# Initializing and loading a pre-trained model
model = JTNNVAE(vocab, hidden_size=450, latent_size=56, depth=20, num_conv=3)
pretrained_model_path = 'icml18-jtnn-master/fast_molvae/moses-h450z56/model.iter-400000'
model.load_state_dict(torch.load(pretrained_model_path))
model = model.cuda()

# Defining the target molecule and computing its fingerprint
target_smiles = 'O=S(=O)(N)c1c(ccc(c1)Nc2nccc(n2)N(c4ccc3c(nn(c3C)C)c4)C)C'
target_molecule = Chem.MolFromSmiles(target_smiles)
target_fingerprint = Chem.GetMorganFingerprintAsBitVect(target_molecule, 2, nBits=2**23)

def evaluate_similarity(input_values):
    encoded_data_part1 = torch.randn(1, 28).cuda()
    encoded_data_part2 = torch.randn(1, 28).cuda()
    
    # Setting values for encoded_data_part1 and encoded_data_part2 from input_values
    for idx, value in enumerate(input_values[:28]):
        encoded_data_part1[0][idx] = value
    for idx, value in enumerate(input_values[28:]):
        encoded_data_part2[0][idx] = value
    
    # Decoding to SMILES string and converting to molecule
    decoded_smiles = model.decode(encoded_data_part1, encoded_data_part2, False)
    decoded_molecule = Chem.MolFromSmiles(decoded_smiles)
    
    # Computing fingerprint and similarity score
    decoded_fingerprint = Chem.GetMorganFingerprintAsBitVect(decoded_molecule, 2, nBits=2**23)
    similarity_score = Chem.DataStructs.TverskySimilarity(decoded_fingerprint, target_fingerprint, 0.5, 0.01)
    
    return -similarity_score  # EvoTorch minimizes, so we take the negative of the score

# Create a Problem instance to solve
problem = Problem("min", evaluate_similarity, solution_length=56, initial_bounds=(-1, 1))

# Create a SearchAlgorithm instance to optimise the Problem instance
searcher = SNES(problem, stdev_init=5)

# Create loggers as desired
stdout_logger = StdOutLogger(searcher)  # Status printed to the stdout
pandas_logger = PandasLogger(searcher)  # Status stored in a Pandas dataframe

# Running the optimization algorithm
start_time = time.time()
searcher.run(30)  # Running for 30 iterations as an example
end_time = time.time()

# Processing the information accumulated by the loggers
progress = pandas_logger.to_dataframe()
progress.mean_eval.plot()  # Display a graph of the evolutionary progress by using the pandas data frame

# Saving the results to file
with open('JTVAE_results.txt', 'w') as file:
    for index, row in progress.iterrows():
        file.write(f"Generation: {index}, Fitness: {-row['mean_eval']}, Stdev: {row['stdev']}\n")

# Printing total runtime
print(f"Total runtime: {end_time - start_time} seconds")
