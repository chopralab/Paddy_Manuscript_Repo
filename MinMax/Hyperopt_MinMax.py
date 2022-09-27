import math
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import random
import numpy as np
import time

np.random.seed(5)
rs=np.random.RandomState(5)
random.seed(5)

def f_2(params):
    x=params['x']
    y=params['y']
    r1=((x-0.5)**2)+((y-0.5)**2)
    r2=((x-0.6)**2)+((y-0.1)**2)
    result = (0.80*math.exp(-(r1)/(0.3**2))) + (0.88*math.exp(-(r2)/0.03**2))
    #global maximum at (0.6,0.1) with local at (0.5,0.5)
    return (-result)

fspace = { 'x' : hp.uniform('x', 0, 1) , 'y' : hp.uniform('y', 0, 1) }

g = 0
c = 0
b_list = []
while c < 100:
    start = time.time()
    best = fmin(fn=f_2, space=fspace, algo=tpe.suggest, max_evals=500, rstate=rs)
    e = time.time()
    b = [best,f_2(best),e-start]
    b_list.append(b)
    if f_2(best) <  -0.81:
        g +=1
        print(best)
    print(g,c)
    c+=1

hp_minmax_results = np.array(b_list)

np.save("Hyperopt_MinMax",hp_minmax_results)

