import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['axes.spines.right'] = False
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.linewidth'] = 1.5
matplotlib.use('Agg')
import paddy


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

file_name = 'Hyperopt_Tversky.txt'
f = open("Hyperopt_Tversky.txt","r")

fl = file_len(file_name)

f = open("hyperopt_vae_T_3500_timed.txt","r")
hp_T = []
hp_b = 0
c = 0 
while c < 3500:
	line = f.readline().strip()
	if float(line.split(':')[-1]) > hp_b:
		hp_b = float(line.split(':')[-1])
	hp_T.append([hp_b,-float(line.split(',')[1])])
	c +=1



file_name = 'Paddy_Tversky_Pop.txt'
f = open("Paddy_Tversky_Pop.txt","r")

fl = file_len(file_name)

PP_T = []
hp_b = 0
c = 0
fl = fl -2 
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy is done!':
		c+=1
		break
	if float(line.split(':')[-1]) > hp_b:
		hp_b = float(line.split(':')[-1])
	PP_T.append([hp_b,-float(line.split(',')[1])])
	c +=1


file_name = 'Paddy_Tversky_Gen.txt'
f = open("Paddy_Tversky_Gen.txt","r")

fl = file_len(file_name)

PG_T = []
hp_b = 0
c = 0 
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy is done!':
		c+=1
		break
	if float(line.split(':')[-1]) > hp_b:
		hp_b = float(line.split(':')[-1])
	PG_T.append([hp_b,-float(line.split(',')[1])])
	c +=1


PG_T = np.array(PG_T)
PP_T = np.array(PP_T)
hp_T = np.array(hp_T)


plt.plot(hp_T[:,1],hp_T[:,0],c='#8ac6d1ff',label='Hyperopt')
#plt.plot(PG_T[:,1],PG_T[:,0],c='#e6a157ff',label='Paddy (Generational)')
plt.plot(PP_T[:,1],PP_T[:,0],c='#eb6934ff',label='Paddy (Population)')
plt.plot([hp_T[0,1],hp_T[-1,1]],[0.669344042838,0.669344042838],linestyle='--',c='#808080ff',label='Random')
plt.xlabel('Runtime (Seconds)',fontsize=18)
plt.ylabel('Tversky Similarity',fontsize=18)
plt.yticks([0.3,0.4,0.5,0.6,0.7,0.8],fontsize=13)
plt.xticks(fontsize=13)
plt.title('Tversky Similarity Optimization',fontsize=22)
plt.legend(loc='lower right',fontsize=12)
plt.tight_layout()
#plt.savefig(filename='vae_tv.svg',dpi=600)
plt.show()


### Custom metric

file_name = 'Hyperopt_Custom.txt'
f = open("Hyperopt_Custom.txt","r")

fl = file_len(file_name)

f = open("Hyperopt_Custom.txt","r")
hp_C = []
hp_b = 0
c = 0 
while c < 3500:
	line = f.readline().strip()
	if float(line.split(':')[-1]) > hp_b:
		hp_b = float(line.split(':')[-1])
	hp_C.append([hp_b,-float(line.split(',')[1])])
	c +=1



file_name = 'Paddy_Custom_Pop.txt'
f = open("Paddyt_Custom_Pop.txt","r")

fl = file_len(file_name)

PP_C = []
hp_b = 0
c = 0 
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy is done!':
		c+=1
		break
	if float(line.split(':')[-1]) > hp_b:
		hp_b = float(line.split(':')[-1])
	PP_C.append([hp_b,-float(line.split(',')[1])])
	c +=1


file_name = 'Paddy_Custom_Gen.txt'
f = open("Paddy_Custom_Gen.txt","r")

fl = file_len(file_name)

PG_C = []
hp_b = 0
c = 0 
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy is done!':
		c+=1
		break
	if float(line.split(':')[-1]) > hp_b:
		hp_b = float(line.split(':')[-1])
	PG_C.append([hp_b,-float(line.split(',')[1])])
	c +=1


PG_C = np.array(PG_C)
PP_C = np.array(PP_C)
hp_C = np.array(hp_C)


plt.plot(hp_C[:,1],hp_C[:,0],c='#8ac6d1ff',label='Hyperopt')
#plt.plot(PG_C[:,1],PG_C[:,0],c='#e6a157ff',label='Paddy (Generational)')
plt.plot(PP_C[:,1],PP_C[:,0],c='#eb6934ff',label='Paddy (Population)')
plt.plot([hp_C[0,1],hp_C[-1,1]],[1.9669190248,1.9669190248],linestyle='--',c='#808080ff',label='Random')
plt.xlabel('Runtime (Seconds)',fontsize=18)
plt.ylabel('Multi Feature Objective Score',fontsize=12)
plt.yticks([1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8],fontsize=13)
plt.xticks(fontsize=13)
plt.title('Multi Feature Molecule Optimization',fontsize=22)
plt.legend(loc='lower right',fontsize=12)
plt.tight_layout()
#plt.savefig(filename='vae_MF.svg',dpi=600)
plt.show()


