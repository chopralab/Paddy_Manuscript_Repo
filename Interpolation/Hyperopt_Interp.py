import math
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import random
import numpy as np 
import time

np.random.seed(5)
rs=np.random.RandomState(5)
random.seed(5)


def gramacy_lee():
    x = -0.5
    y=[]
    c=0
    xs = []
    xp = np.arange(-.5,2.501,0.001)
    while c <len(xp):
        xs.append(round(xp[c],3))
        c = c+1
    c=0
    while c < len(xp):
        y.append(((math.sin(10*math.pi*x))/(2*x))+((x-1)**4))
        x = x +.001
        c = c+1
    return xs,y 

x,yp = gramacy_lee()

def trig_inter_hp(params,x=x,yp=yp):
    if len(params) % 2 == 0:
        print ("must use odd value for dim greater than 1!")
        return
    c = 0
    s_x = []
    while c < len(x):
        ###this evaluates over x
        n = 1
        xn_out = []
        while n <= ((len(params)-1)/2):
            ###evaluates sums of cos and sin
            a = ((n*2)-1)
            b=(n*2)
            temp_y = (params['x{0}'.format(a)]*(math.cos((n*x[c]))))+((params['x{0}'.format(b)])*(math.sin((n*x[c]))))
            xn_out.append(temp_y)
            n = n+1
        xn_out.append(params['x0'])
        s_x.append(sum(xn_out))
        c = c + 1
    c = 0 
    error = []
    while c < len(x):
        error.append((abs(yp[c]-s_x[c]))**2)
        c = c+1
    ave_error = sum(error)/(len(yp))
    return (ave_error)


def trig_inter(seed,x):
    if len(seed) % 2 == 0:
        print ("must use odd value for dim greater than 1!")
    c = 0
    output = []
    s_x = []
    while c < len(x):
        ###this evaluates over x ###
        k = 1
        xn_out = []
        while k < ((len(seed)-1)/2):
            ###evaluates sums of cos and sin
            a = ((k*2)-1)
            b=(k*2)
            temp_y = ((seed['x{0}'.format(a)])*(math.cos((k*x[c]))))+((seed['x{0}'.format(b)])*(math.sin((k*x[c]))))
            xn_out.append(temp_y)
            k = k+1
        xn_out.append(seed['x0'])
        s_x.append(sum(xn_out))
        c = c + 1
    return(s_x)

def polly_plot(x,y,p):
    plt.plot(x,y)
    y2=trig_inter(p,x)
    plt.plot(x,y2)
    plt.show()


def pspace_maker(leng):
    c = 0
    pspace = {}
    while c < leng:
        pspace['x{0}'.format(c)]= hp.uniform('x{0}'.format(c),-1,1)
        c += 1
    return (pspace)

fspace = pspace_maker(65)


c = 0
b_list = []
while c < 100:
    start = time.time()
    best = fmin(fn=trig_inter_hp, space=fspace, algo=tpe.suggest, max_evals=1500, rstate=rs)
    e = time.time()
    b = [best,trig_inter_hp(best),e-start]
    b_list.append(b)
    print(c)
    c+=1

p1 = [] 
p2 =[]
for i in b_list:
	p1.append(i[1])
	p2.append(i[2])

np.save('Hyperopt_Interp',b_list)
