from tensorflow import set_random_seed
import random
import itertools
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
import os
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())


'''
10.1.168-0 --> 9.0-h13b8566_0

'''
dataframe = pd.read_csv("/storage/armen_beck/d4990.csv", header=None)
dataset = dataframe.values
X = dataset[:,1:].astype(int)
Y = dataset[:,0]
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)
y = dummy_y


fspace = {'leng_1':hp.quniform('leng_1',300,3000,1), 'dropout_1':hp.uniform('dropout_1',0,1),'leng_2':hp.quniform('leng_2',32,2000,1),'dropout_2':hp.uniform('dropout_2',0,1)}


def createmodel():
	model = Sequential()
	l1=np.random.randint(300,3000)
	l2 = np.random.randint(32,2000)
	d1 = np.random.uniform(0,1)
	d2 =np.random.uniform(0,1)
	model.add(Dense(l1, activation='relu', input_dim=2048))
	model.add(Dropout(d1))
	model.add(Dense(l2, activation='relu'))
	model.add(Dropout(d2))
	model.add(Dense(30, activation='softmax'))
	params = [l1,l2,d1,d2]
	# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy',
	              optimizer='adam')
	return model , params



def run_func():
	p_start = time.time()
	kfold = StratifiedKFold(n_splits=3,shuffle=True,random_state=4)
	ls=[]
	trainls=[]
	for train_index, val_index in kfold.split(X, encoded_Y):
		temp_ls = []
		keras.backend.clear_session()
		model, params = createmodel()
		X_train, X_val = X[train_index], X[val_index]
		y_train, y_val = y[train_index], y[val_index]
		model.fit(X_train, y_train, validation_data=(X_val,y_val),epochs=5, batch_size=1000,verbose=None)
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
	print(ls)
	print(p_start-start)		
	return(sum(ls)/3,params)


bs_counter = 0
while bs_counter < 100:
	trials = Trials()
	start = time.time()
	best = 0
	c2 = 0
	best_p = []
	while c2 < 200:
		run , params = run_func()
		if run > best:
			best = run
			best_p = params
		c2 += 1
	end = time.time()
	print('info to parse')
	print(end-start)
	print(best)
	print(best_p)
	bs_counter +=1 





