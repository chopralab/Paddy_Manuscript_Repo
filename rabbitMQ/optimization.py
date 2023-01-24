#Optimization Module for the optimizer 


#edbo imports
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# /mnt/c/Users/sanjay iyer
import os
import shutil
import subprocess
import time
sys.path.append('/home/sanjay/github/AFRL/git_edbo/edbopaper/edbo/')
from plus.optimizer_botorch import EDBOplus



def initialize_optimization():
    print('|Initialize| Bayesian Optimization program started')
    components = {
                'enzyme_conc':[44,1,2,4,8,16,18,20,24],   # Discrete grid of enzyme concentrations
                'substrate_conc': [27,1,2,4,8,10,12,14,16], # discrete space of substrate concentration
                'incubation_time': [315,5,15,30,60,120,180,240,480]} #discrete space of incubation time

    #initialize a scope for beginning a run
    scope = EDBOplus.generate_reaction_scope(components=components)
    #Set objectives to optimize, min/max, batch size
    args = {'objectives': ['assay_optimization_score'], 'objective_mode': ['max'], 'batch': 1, 'seed': 42}

#step 3 update results with aos
def results_update(aos):
    df = pd.read_csv('reaction.csv')
    time.sleep(3)
    # df['assay_optimization_score'][0] = aos
    df.loc[0,('assay_optimization_score')] = aos
    df.to_csv('reaction.csv',index=False)

#Run BO
#requires csv of parameter space 
def bo_run():
    df = pd.read_csv('reaction.csv')
    bo = EDBOplus()
    args = {'objectives': ['assay_optimization_score'], 'objective_mode': ['max'], 'batch': 1, 'seed': 42}
    bo.run(**args)
    time.sleep(5)
    # print('Optimizer selected new parameters to run next:\n{}'.format(df.iloc[0,[0,1,2]]))
    print('Optimizer selected new parameters to run next:\n{}'.format(df.iloc[0,[0,1,2]].to_string()))
    return (df['enzyme_conc'][0],df['substrate_conc'][0],df['incubation_time'][0])








#older paddy code
# # /home/sanjay/github/paddy/Paddy_Manuscript_Repo
# np.random.seed(5)
# rs=np.random.RandomState(5)
# random.seed(5)

# enzyme_conc = (0,0.25, 0.5,1,2,4,8,16) #nM
# substrate_conc = (0,0.125,0.25,0.5,1,2,4,8) #uM
# incubation_time = (5,15,30,60,120,180,240,480) #min

# enzyme_param = 
# substrate_param =
# incubation_param = 

# #Timer.sleep to setup a delay 
