####
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import set_random_seed
import itertools
import random
import pandas as pd 
import keras
import time
import numpy
seed = 7
numpy.random.seed(seed)
set_random_seed(2)
random.seed(1)
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.metrics import accuracy_score,f1_score
from sklearn.model_selection import train_test_split
import numpy as np 
from sklearn.model_selection import KFold,GroupKFold
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
#from IPython.display import SVG,display
from keras.utils.vis_utils import model_to_dot
#import matplotlib.pyplot as plt 
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from keras.models import model_from_json

from tensorflow import set_random_seed
import sys
sys.path.append('paddy/')
import paddy
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from tensorflow import logging
from tensorflow.python.client import device_lib
# print('c',device_lib.list_local_devices())

logging.set_verbosity(logging.ERROR) #get rid of messages?

seed = 7
numpy.random.seed(seed)
set_random_seed(2)
random.seed(1)
dataframe = pd.read_csv("MLP_Hyperparameter_Optimization/d4990.csv", header=None)
dataset = dataframe.values
X = dataset[:,1:].astype(int)
Y = dataset[:,0]
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)
y = dummy_y

earlystopping=keras.callbacks.EarlyStopping(monitor='val_loss',
                              min_delta=0,
                              patience=5,
                              verbose=0, mode='auto')


def createmodel(values):
	values = values
	model = Sequential()
	model.add(Dense(int(values[1][0]), activation='relu', input_dim=2048)) #size of layers | dimensionality
	model.add(Dropout(values[0][0])) # connectivity 
	model.add(Dense(int(values[3][0]), activation='relu'))
	model.add(Dropout(values[2][0]))
	model.add(Dense(30, activation='softmax'))
	# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy',
	              optimizer='adam')
	return model



def run_func(values):
	time.sleep(3)
	print('____________________________')
	print('Starting New Optimization Iteration')
	print('____________________________')
	print('____________________________')
	time.sleep(4)
	start_p = time.time()
	kfold = StratifiedKFold(n_splits=3,shuffle=True,random_state=4)
	ls=[]
	trainls=[]
	print('Hyperparameters being tuned')
	print('Hidden layer 1 size:', values[1][0]) #printing out hidden layer size and dropouts 
	print('Hidden layer 1 dropout:', values[0][0])
	print('Hidden layer 2 size:', values[3][0])
	print('Hidden layer 1 dropout:', values[2][0])
	print('____________________________')
	print('____________________________')
	time.sleep(4)
	for train_index, val_index in kfold.split(X, encoded_Y):
		temp_ls = []
		keras.backend.clear_session()
		model = createmodel(values) #values list of hyper parameters
		X_train, X_val = X[train_index], X[val_index]
		y_train, y_val = y[train_index], y[val_index]
		model.fit(X_train, y_train, validation_data=(X_val,y_val),epochs=5, batch_size=1000, verbose=False)
		preds = model.predict(X_val)
		preds = preds.argmax(axis=1)
		train = model.predict(X_train)
		train = train.argmax(axis=1)	
		#preds[preds>=0.5] = 1
		#preds[preds<0.5] = 0
		#for i,col in enumerate(Y.columns):
		#temp_ls.append()
		ls.append(f1_score(encoded_Y[val_index],preds,average='micro'))
		trainls.append(f1_score(encoded_Y[train_index],train,average='micro'))
	print('Hyperparameter Optimization 3-Fold F1 Scores')
	print('Fold 1 F1 Score:',ls[0])
	print('Fold 2 F1 Score:',ls[1])
	print('Fold 3 F1 Score:',ls[2]) #list of f1 scores
	print('_______________________________')
	print('_______________________________')
	# print('a',start-time.time()) #timer to log iteration
	return(sum(ls)/3)


dropout = paddy.PaddyParameter(param_range=[0,.5,.05], param_type='continuous', limits=[0, 1], gaussian='default',normalization = True)
dropout2 = paddy.PaddyParameter(param_range=[0,.5,.05], param_type='continuous', limits=[0, 1], gaussian='default',normalization = True)
layer1 = paddy.PaddyParameter(param_range=[500,1000,5], param_type='integer', limits=[300, 3000], gaussian='default',normalization = True)
layer2 = paddy.PaddyParameter(param_range=[32,500,5], param_type='integer', limits=[30, 2000], gaussian='default',normalization = True)

class space(object):
	def __init__(self):
		self.d1 = dropout #layer 1 connectivity
		self.l1 = layer1  #layer 1 size
		self.d2 = dropout2 #layer 2 connectivity
		self.l2 = layer2  #layer 2 size

test_space = space()
bs_counter = 0
while bs_counter < 2:
	start = time.time()
	runner = paddy.PFARunner(space=test_space, eval_func=run_func,
		            paddy_type='generational', rand_seed_number=5,
		            yt=3,Qmax=2,r=.2,iterations =2)
	runner.run_paddy() #verbose='all' was taken out
	e = time.time()
	# print('d',e-start) #timing of each iteration
	bs_counter += 1

# print('b',ls)
# print('a',start-time.time())

#seed 25, iteration 7, qmax 10, yt 5, bs_couter <100

