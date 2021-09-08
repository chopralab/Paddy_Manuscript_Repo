import numpy as np
import matplotlib.pyplot as plt
import math


def rmse(inputv):
	ave = sum(inputv)/100
	temp = []
	for i in inputv:
		temp.append((ave-i)**2)
	return((sum(temp)/100)**.5)

paddy_trig = np.load('Paddy_Interp.npy')

pe = [] 
pt =[]
for i in paddy_trig:
	pe.append(-i[1])
	pt.append(i[2])

hp_trig = np.load('Hyperopt_Interp.npy')

he = [] 
ht =[]
for i in hp_trig:
	he.append(i[1])
	ht.append(i[2])



random_trig = np.load('Random_Interp.npy')

re = [] 
rt =[]
for i in random_trig:
	re.append(i[1])
	rt.append(i[2])


plt.scatter(pt,pe,c='#e6a157ff',edgecolors='#eb6934ff',label='Paddy')
plt.scatter(ht,he,c='#8ac6d1ff',edgecolors='#1f77b4ff',label='Hyperopt')
plt.scatter(rt,re,c='#808080ff',edgecolors='#3a3a3aff',label='Random')
plt.ylabel('MSE',fontsize=17)
plt.xlabel('Runtime (Seconds)',fontsize=18)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)
plt.title('Gramacy & Lee Interpolation',fontsize=22)
plt.legend(loc='lower right',fontsize=12)
plt.tight_layout()
#plt.savefig(filename='glruntime.svg',dpi=600)
plt.show()

#best paddy trig



def gramacy_lee():
    x = -0.5
    y=[]
    c=0
    xs = []
    xp = np.arange(-.5,2.501,0.001)
    while c < len(xp):
        xs.append(round(xp[c],3))
        c = c+1
    c=0
    while c < len(xp):
        y.append(((math.sin(10*math.pi*x))/(2*x))+((x-1)**4))
        x = x +.001
        c = c+1
    return xs,y 

x,y = gramacy_lee()


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

hpbp = hp_trig[np.argmin(hp_trig[:,1]),0] #parameters for the best hyperopt trial
hy = trig_inter(hpbp,x)


plt.plot(x,y,c='#808080ff',label='Gramacy & Lee')
plt.plot(x,hy,c='#8ac6d1ff',label='Hyperopt')
plt.xlabel('x',fontsize=18)
plt.ylabel('y',fontsize=18)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)
plt.title('Gramacy & Lee Interpolation\n (Hyperopt)',fontsize=22)
plt.legend(loc='upper right',fontsize=12)
plt.tight_layout()
#plt.savefig(filename='glhp.svg',dpi=600)
plt.show()



def p_trig_inter(seed,x):
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


pbp = paddy_trig[np.argmax(paddy_trig[:,1]),0] # parameters for the best paddy trial
pbp = pbp[:,0]
py = p_trig_inter(pbp,x)

plt.plot(x,y,c='#808080ff',label='Gramacy & Lee')
plt.plot(x,py,c='#eb6934ff',label='Paddy')
plt.xlabel('x',fontsize=18)
plt.ylabel('y',fontsize=18)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)
plt.title('Gramacy & Lee Interpolation\n (Paddy)',fontsize=22)
plt.legend(loc='upper right',fontsize=12)
plt.tight_layout()
#plt.savefig(filename='glpaddy.svg',dpi=600)
plt.show()

rbp = random_trig[np.argmin(random_trig[:,1]),0] # parameters for the best random trial
ry = p_trig_inter(rbp,x)

plt.plot(x,y,c='#808080ff',label='Gramacy & Lee')
plt.plot(x,ry,c='#3a3a3aff',label='Random')
plt.xlabel('x',fontsize=18)
plt.ylabel('y',fontsize=18)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)
plt.title('Gramacy & Lee Interpolation\n (Paddy)',fontsize=22)
plt.legend(loc='upper right',fontsize=12)
plt.tight_layout()
#plt.savefig(filename='glpaddy.svg',dpi=600)
plt.show()

