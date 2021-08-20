import math
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import random
import paddy
import numpy as np 
import time

np.random.seed(5)
rs=np.random.RandomState(5)
random.seed(5)

def function_2(input):
    x=input[0,0]
    y=input[1,0]
    r1=((x-0.5)**2)+((y-0.5)**2)
    r2=((x-0.6)**2)+((y-0.1)**2)
    result = (0.80*math.exp(-(r1)/(0.3**2))) + (0.88*math.exp(-(r2)/0.03**2))
    #global maximum at (0.6,0.1) with local at (0.5,0.5)
    return (result)

i = ['generational', 'scaled', 50, 100, 5, False]

y_param = paddy.PaddyParameter(param_range=[0,1,.01],param_type='continuous',limits=[0,1,.1], gaussian=i[1],normalization = i[5])
x_param = paddy.PaddyParameter(param_range=[0,1,.01],param_type='continuous',limits=[0,1,.1], gaussian=i[1],normalization = i[5])
class space(object):
        def __init__(self):
                self.xp = x_param
                self.yp = y_param

test_space = space()
c = 0
g = 0
r_list = []
while c<100:
    runner = paddy.PFARunner(space=test_space, eval_func=function_2,
                            paddy_type=i[0], rand_seed_number=i[2],
                            yt=i[2],Qmax=i[3],r=.02,iterations =i[4])
    s = time.time()
    runner.run_paddy()
    e = time.time() - s
    if max(runner.seed_fitness) > 0.81:
        g +=1
    print(g,c)
    f=(max(runner.seed_fitness))
    p=runner.seed_params[np.argmax(runner.seed_fitness)]
    r_list.append([p,f,e])
    c += 1


p1 = [] 
p2 =[]
for i in r_list:
        p1.append(i[1])
        p2.append(i[2])

np.save("Paddy_MinMax",r_list)

