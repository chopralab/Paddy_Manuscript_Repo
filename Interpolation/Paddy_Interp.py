import sys
sys.path.append('paddy/')
import paddy
from paddy import Paddy_Parameter
from paddy.Paddy_Parameter import *
from paddy import Paddy_Runner
from paddy import Default_Numerics
import numpy as np
import random
import time

np.random.seed(5)
rs=np.random.RandomState(5)
random.seed(5)



run_func = paddy.Default_Numerics.EvalNumeric()
test_polly_space = paddy.Default_Numerics.Polynomial(length=65,scope=1,gausian_type='default',normalization=False)
c = 0
r_list = []
while c < 100:
    test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
    rand_seed_number = 25, yt = 25, paddy_type = 'generational' , Qmax = 25  , r = .02 , iterations = 10)
    start=time.time()
    test_runner.run_paddy()
    e = time.time()
    p=test_runner.seed_params[np.argmax(test_runner.seed_fitness)]
    r = [p,max(test_runner.seed_fitness),e-start]
    r_list.append(r)
    print(sum(np.array(r_list)[:,1])/len(r_list),sum(np.array(r_list)[:,2])/len(r_list))
    c += 1

p1 = [] 
p2 =[]
for i in r_list:
	p1.append(i[1])
	p2.append(i[2])

np.save("Paddy_Interp",r_list)
