# import math
# import numpy as np
# import pika, sys, os

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

sys.path.append('/home/sanjay/github/Paddy2/Paddy_Manuscript_Repo/rabbitMQ')

#create df from reaction csv
df = pd.read_csv('reaction.csv')
aos_global = [0]

#step 1 take in df as input and return optimized parameters for instrument to run
def aos_input(df):
    aos_input = (df['enzyme_conc'][0],df['substrate_conc'][0],df['incubation_time'][0])
    print('AOS input parameters:\n Enzyme Concentration = {} \n Substrate Concentration = {} \n Incubation_Time = {}'.format(aos_input[0],aos_input[1],aos_input[2]))
    return aos_input

#Step 2 take in aos_input and calculate AOS   
#update csv
#enzyme_conc, substrate_conc, incubation_time
def assay_optimization_score(enzyme_conc,substrate_conc,incubation_time):
    aos = 10000*min(max(0.52-0.495,0),0.025)/((25*enzyme_conc) + (5*substrate_conc) + (incubation_time))
    #z < 0.52 undesirable
    #time.sleep(1)
    aos_global[0] = aos
    return aos

####moved to optimizer    
# #step 3 update results with aos
# def results_update():
#     time.sleep(3)
#     df['assay_optimization_score'][0] = float(aos_global[0])
#     print('Updated Assay Optimization Score: \n', df.iloc[[0]])
#     df.to_csv('reaction.csv',index=False)
#     return float(aos_global[0])

def run_all():
    aos_input(df)
    assay_optimization_score(aos_input)
    # results_update()






###older code
# def assay_optimization_score(enzyme_conc, substrate_conc, incubation_time):
#     aos = 10000*min(max(0.52-0.495,0),0.025)/((25*enzyme_conc) + (5*substrate_conc) + (incubation_time))
#     #z < 0.52 undesirable
#     return aos


# def results_update_csv(aos):
#     df = pd.read_csv('reaction.csv')

# #Timer.sleep to setup a delay 