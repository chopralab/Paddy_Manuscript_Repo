#import all the modules needed
#paddy imports
import sys
import math
import random
#Append the 
sys.path.append('/home/sanjay/github/Paddy/Paddy_Manuscript_Repo/paddy')
import paddy
import numpy as np 
import time
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
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
# import instrument


def initialize_optimization():
    components = {
                'enzyme_conc':[0,0.25, 0.5,1,2,4,8,16],   # Discrete grid of concentrations
                'substrate_conc': [0,0.125,0.25,0.5,1,2,4,8],
                'incubation_time': [5,15,30,60,120,180,240,480]}

    scope = EDBOplus.generate_reaction_scope(components=components)
    args = {'objectives': ['assay_optimization_score'], 'objective_mode': ['max'], 'batch': 1, 'seed': 42}

#step 3 update results with aos
def results_update(aos):
    df = pd.read_csv('reaction.csv')
    time.sleep(3)
    df['assay_optimization_score'][0] = aos
    print('Updated Assay Optimization Score: \n', df.iloc[[0]])
    df.to_csv('reaction.csv',index=False)

def bo_run():
    df = pd.read_csv('reaction.csv')
    bo = EDBOplus()
    args = {'objectives': ['assay_optimization_score'], 'objective_mode': ['max'], 'batch': 1, 'seed': 42}
    bo.run(**args)
    # df = pd.read_csv('reaction.csv')
    time.sleep(5)
    print('Assay Parameters Updated: \n', df.iloc[[0]])
    return (df['enzyme_conc'][0],df['substrate_conc'][0],df['incubation_time'][0])

# results_update()
# bo_run()








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
