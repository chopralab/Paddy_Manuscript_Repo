import numpy as np
import matplotlib.pyplot as plt


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

file_name = 'hyperopt_100_timed_2.txt'
f =  open("hyperopt_100_timed_2.txt","r")

fl = file_len(file_name)

yf = []
xf = []
f = open("hyperopt_100_timed_2.txt","r")
hp_dic = {}
c = 0
cls_c = 0
f1=[]
rt=[]
rtt = []
f1tt = []
while c < fl:
	line=f.readline()
	if line[0] == '-':
		rtt.append(-float(line))
	elif line[0] == '[':
		yt=(line.strip()).strip('][').split(', ')
		ytt = []
		for i in yt:
			ytt.append(float(i))
		f1tt.append(sum(ytt)/3.0)
	elif line[0] == '{':
		rt.append(max(rtt))
		f1.append(max(f1tt))
		rtt=[]
		f1tt=[]
	c+=1		
	


c = 0
f = open("paddy_100_timed.txt","r")
x = [] 
y = []
yf = []
xf = []


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

file_name = 'paddy_100_timed.txt'

fl = file_len(file_name)
c = 0
fls = [] #lines to denote when a run is done
while c < fl:
	line=f.readline()
	if len(line) > 2:
		if line[-2] == '!':
				fls.append(c)
	c += 1


f = open("paddy_100_timed.txt","r")
c = 0
cls = [] #lines to denote when an evaluation is done
while c < fl:
	line=f.readline().split(' ')
	if line[-1] == 'complete\n':
			cls.append(c)
	c += 1



yf = []
xf = []
f = open("paddy_100_timed.txt","r")
paddy_dic = {}
c = 0
cls_c = 0
fls_c = 0
while c < fl:
	if fls_c == 100:
		break
	if cls_c<len(cls):
		logic = 0
		if c==cls[cls_c]-2:
			yt=(f.readline().strip()).strip('][').split(', ')
			ytt = []
			for i in yt:
				ytt.append(float(i))
			yf.append(sum(ytt)/3.0)
		elif c==cls[cls_c]-1:
			xt=(f.readline().strip()).strip('][').split(', ')
			xf.append(float(xt[0]))
			cls_c +=1
		elif c == fls[fls_c]-2:
			xt=(f.readline().strip()).strip('][').split(' ')
			paddy_dic['{0}_best'.format(fls_c)] =float(xt[-1])
			paddy_dic['{0}_runtime'.format(fls_c)] = xf
			paddy_dic['{0}_F1'.format(fls_c)] = yf
			fls_c +=1
			xf = []
			yf = []
		else:
			f.readline()
		c+=1
	else:
		if c == fls[fls_c]-2:
			xt=(f.readline().strip()).strip('][').split(' ')
			paddy_dic['{0}_best'.format(fls_c)] =float(xt[-1])
			paddy_dic['{0}_runtime'.format(fls_c)] = xf
			paddy_dic['{0}_F1'.format(fls_c)] = yf
			fls_c +=1
			xf = []
			yf = []
		else:
			f.readline()
		c+=1



best_list = []
time_list = []		

c = 0
while c < 100:
	best_list.append(max(paddy_dic['{0}_F1'.format(c)]))
	time_list.append(paddy_dic['{0}_runtime'.format(c)][-1])
	c +=1


tl = []
for i in time_list:
	tl.append(-i)



def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

file_name = 'random_solv.txt'
f =  open("random_solv.txt","r")

fl = file_len(file_name)

yf = []
xf = []
f = open("random_solv.txt","r")
hp_dic = {}
c = 0
cls_c = 0
f1_r=[]
rt_r=[]
rtt_r = []
f1tt_r = []
while c < fl:
	line=f.readline()
	if line == 'info to parse\n':
		line=f.readline()
		rt_r.append(float(line))
		line=f.readline()
		yt=(line.strip()).strip('][').split(', ')
		ytt = []
		for i in yt:
			ytt.append(float(i))
		f1_r.append(sum(ytt))
		c+=3
	else:
		c+=1	



plt.scatter(tl,best_list,c='#e6a157ff',edgecolors='#eb6934ff',label='Paddy')
plt.scatter(rt,f1,c='#8ac6d1ff',edgecolors='#1f77b4ff',label='Hyperopt')
plt.scatter(rt_r,f1_r,c='#808080ff',edgecolors='#3a3a3aff',label='Random')
plt.ylabel('F1 Score',fontsize=17)
plt.xlabel('Runtime (Seconds)',fontsize=18)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)
plt.legend(loc='lower left',fontsize=12)
plt.title('Hyperparameter Optimization',fontsize=22)
plt.tight_layout()
#plt.savefig(filename='hyperparams.svg',dpi=600)
plt.show()


def rmse(inputv):
	ave = sum(inputv)/100
	temp = []
	for i in inputv:
		temp.append((ave-i)**2)
	return((sum(temp)/100)**.5)	



