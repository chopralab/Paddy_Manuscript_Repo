import math
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
            temp_y = (params[a]*(math.cos((n*x[c]))))+((params[b])*(math.sin((n*x[c]))))
            xn_out.append(temp_y)
            n = n+1
        xn_out.append(params[0])
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
            temp_y = ((seed[a])*(math.cos((k*x[c]))))+((seed[b])*(math.sin((k*x[c]))))
            xn_out.append(temp_y)
            k = k+1
        xn_out.append(seed[0])
        s_x.append(sum(xn_out))
        c = c + 1
    return(s_x)





c = 0
b_list = []
while c < 100:
    start = time.time()
    best = math.inf
    c2 = 0
    params_b = []
    while c2 < 5000:
        params_i=np.random.uniform(-1,1,65)
        run = trig_inter_hp(params=params_i)
        if run < best:
            best = run
            params_b = params_i    
        c2 += 1
    e = time.time()
    b = [params_b,best,e-start]
    b_list.append(b)
    print(c)
    print(best)
    c+=1

p1 = [] 
p2 =[]
for i in b_list:
	p1.append(i[1])
	p2.append(i[2])

np.save("Random_Interp",b_list)

