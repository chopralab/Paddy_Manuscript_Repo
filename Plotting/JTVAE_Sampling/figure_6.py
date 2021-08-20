#### plotter for figure 6a# needs to be python2 to handle pickles generated in python2 (JTVAE)

##traversky pop
import numpy as np
import matplotlib.pyplot as plt
import paddy

def run_func_1():
    print()

runner = paddy.utils.paddy_recover('Paddy_Tversky_Pop')
tv_p = []
tv_p_b =[]
for i in range(0,31):#there are 30 iterations in these trials
	gen_range=runner.generation_data[str(i)]
	temp = []
	if i != 30:
		for j in range(gen_range[0],gen_range[1]+1):
				temp.append(runner.seed_fitness[j])
		tv_p.append(sum(temp)/(len(temp)+0.0))
		tv_p_b.append(max(temp))
	else:
		#print('something')
		for j in range(gen_range[0],gen_range[1]):
				temp.append(runner.seed_fitness[j])
		tv_p.append(sum(temp)/(len(temp)+0.0))
		tv_p_b.append(max(temp))



r_tvg= paddy.utils.paddy_recover('Paddy_Tversky_Gen')
tv_g = []
tv_g_b =[]
for i in range(0,31):
	gen_range=r_tvg.generation_data[str(i)]
	temp = []
	if i != 30:
		for j in range(gen_range[0],gen_range[1]+1):
				temp.append(r_tvg.seed_fitness[j])
		tv_g.append(sum(temp)/(len(temp)+0.0))
		tv_g_b.append(max(temp))
	else:
		for j in range(gen_range[0],gen_range[1]):
				temp.append(r_tvg.seed_fitness[j])
		tv_g.append(sum(temp)/(len(temp)+0.0))
		tv_g_b.append(max(temp))


plt.plot(range(0,31),tv_p,c='#e6a157ff',linestyle='--',label='Iteration Average (Population)')
plt.plot(range(0,31),tv_p_b,c='#e6a157ff',label='Best in Iteration (Population)')
plt.plot(range(0,31),tv_g,c='#eb6934ff',linestyle='--',label='Iteration Average (Generational)')
plt.plot(range(0,31),tv_g_b,c='#eb6934ff',label='Best in Iteration (Generational)')
plt.plot([0,30],[0.669344042838,0.669344042838],linestyle='--',c='#808080ff',label='Random')
plt.xlabel('Iteration',fontsize=18)
plt.ylabel('Multi Feature Objective Score',fontsize=12)
plt.yticks(fontsize=13)
plt.xticks(range(0,31,2),fontsize=13)
#plt.title('Multi Feature Molecule Optimization',fontsize=22)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()


####




#####objective funct fig 6b
import numpy as np
import matplotlib.pyplot as plt
import paddy

def run_func_1():
    print()

r_op= paddy.utils.paddy_recover('Paddy_Custom_Pop')
op_p = []
op_p_b =[]
for i in range(0,31):
	gen_range=r_op.generation_data[str(i)]
	temp = []
	if i != 30:
		for j in range(gen_range[0],gen_range[1]+1):
				temp.append(r_op.seed_fitness[j])
		op_p.append(sum(temp)/(len(temp)+0.0))
		op_p_b.append(max(temp))
	else:
		for j in range(gen_range[0],gen_range[1]):
				temp.append(r_op.seed_fitness[j])
		op_p.append(sum(temp)/(len(temp)+0.0))
		op_p_b.append(max(temp))



r_og= paddy.utils.paddy_recover('Paddy_Custom_Gen')
og_g = []
og_g_b =[]
for i in range(0,31):
	gen_range=r_og.generation_data[str(i)]
	temp = []
	if i != 30:
		for j in range(gen_range[0],gen_range[1]+1):
				temp.append(r_og.seed_fitness[j])
		og_g.append(sum(temp)/(len(temp)+0.0))
		og_g_b.append(max(temp))
	else:
		for j in range(gen_range[0],gen_range[1]):
				temp.append(r_og.seed_fitness[j])
		og_g.append(sum(temp)/(len(temp)+0.0))
		og_g_b.append(max(temp))



plt.plot(range(0,31),op_p,c='#e6a157ff',linestyle='--',label='Iteration Average (Population)')
plt.plot(range(0,31),op_p_b,c='#e6a157ff',label='Best in Iteration (Population)')
plt.plot(range(0,31),og_g,c='#eb6934ff',linestyle='--',label='Iteration Average (Generational)')
plt.plot(range(0,31),og_g_b,c='#eb6934ff',label='Best in Iteration (Generational)')
plt.plot([0,30],[1.9669190248,1.9669190248],linestyle='--',c='#808080ff',label='Random')
plt.xlabel('Iteration',fontsize=18)
plt.ylabel('Multi Feature Objective Score',fontsize=12)
plt.yticks(fontsize=13)
plt.xticks(range(0,31,2),fontsize=13)
#plt.title('Multi Feature Molecule Optimization',fontsize=22)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

####Figure 6c#### done without correct collors
import numpy as np
import matplotlib.pyplot as plt
import paddy

def run_func_1():
    print()

r_tvp= paddy.utils.paddy_recover('Paddy_Tversky_Pop')


file_name = 'Paddy_Tversky_Pop.txt'
f = open("Paddy_Tversky_Pop.txt","r")

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

fl = file_len(file_name)


def it_ret(runner,counter):
	for i in runner.generation_data:
		gen_range=runner.generation_data[i]
		if counter in range(gen_range[0],gen_range[1]+1):
			return(i)



rand_val = 0.669344042838
tvps = []
tvpi = []
tvpsm =[]
c = 0  
fl = fl-2
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy is done!':
		c+=1
		break
	if float(line.split(':')[-1]) > rand_val:
		if float(line.split(':')[-1]) in tvps:
			if line.split(',')[0] in tvpsm:
				pass
			else:
				tvps.append(float(line.split(':')[-1]))
				tvpsm.append(line.split(',')[0])
				it = it_ret(r_tvp,c)
				tvpi.append(int(it))
		else:
			tvps.append(float(line.split(':')[-1]))
			tvpsm.append(line.split(',')[0])
			it = it_ret(r_tvp,c)
			tvpi.append(int(it))
	c +=1





def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


r_tvg= paddy.utils.paddy_recover('Paddy_Tversky_Gen')
file_name = 'Paddy_Tversky_Gen.txt'
f = open("Paddy_Tversky_Gen.txt","r")


fl = file_len(file_name)

def it_ret(runner,counter):
	for i in runner.generation_data:
		gen_range=runner.generation_data[i]
		if counter in range(gen_range[0],gen_range[1]+1):
			return(i)

rand_val = 0.669344042838
tvgs = []
tvgi = []
tvgsm =[]
c = 0
fl = fl -2  
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy is done!':
		c+=1
		break        
	if float(line.split(':')[-1]) > rand_val:
		if float(line.split(':')[-1]) in tvgs:
			if line.split(',')[0] in tvgsm:
				pass
			else:
				tvgs.append(float(line.split(':')[-1]))
				tvgsm.append(line.split(',')[0])
				it = it_ret(r_tvg,c)
				tvgi.append(int(it))
		else:
			tvgs.append(float(line.split(':')[-1]))
			tvgsm.append(line.split(',')[0])
			it = it_ret(r_tvg,c)
			tvgi.append(int(it))
	c +=1


plt.scatter(tvpi,tvps,label='Unique Solutions (Population)') 
plt.scatter(tvgi,tvgs,label='Unique Solutions (Generational)') 
plt.plot([0,30],[0.669344042838,0.669344042838],linestyle='--',c='#808080ff',label='Random')
plt.xlabel('Iteration',fontsize=18)
plt.ylabel('Tversky Similarity',fontsize=18)
plt.yticks(fontsize=13)
plt.xticks(range(0,31,2),fontsize=13)
plt.title('Tversky Similarity Optimization',fontsize=22)
plt.legend(loc='lower right',fontsize=12)
plt.tight_layout()
#plt.savefig(filename='vae_tv_gen.svg',dpi=600)
plt.show()



######





####Figure 6d
import numpy as np
import matplotlib.pyplot as plt
import paddy

def run_func_1():
    print()



def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


r_op= paddy.utils.paddy_recover('Paddy_Custom_Pop')

file_name = 'Paddy_Custom_Pop.txt'
f = open("Paddy_Custom_Pop.txt","r")

fl = file_len(file_name)

def it_ret(runner,counter):
	for i in runner.generation_data:
		gen_range=runner.generation_data[i]
		if counter in range(gen_range[0],gen_range[1]+1):
			return(i)

rand_val = 1.9669190248
ops = []
opi = []
opsm =[]
c = 0  
fl = fl -2
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy is done!':
		c+=1
		break
	if float(line.split(':')[-1]) > rand_val:
		if float(line.split(':')[-1]) in ops:
			if line.split(',')[0] in opsm:
				pass
			else:
				ops.append(float(line.split(':')[-1]))
				opsm.append(line.split(',')[0])
				it = it_ret(r_op,c)
				opi.append(int(it))
		else:
			ops.append(float(line.split(':')[-1]))
			opsm.append(line.split(',')[0])
			it = it_ret(r_op,c)
			opi.append(int(it))
	c +=1



r_og = paddy.utils.paddy_recover('Paddy_Custom_Gen')
file_name = 'Paddy_Custom_Gen.txt'
f = open("Paddy_Custom_Gen.txt","r")



fl = file_len(file_name)

def it_ret(runner,counter):
	for i in runner.generation_data:
		gen_range=runner.generation_data[i]
		if counter in range(gen_range[0],gen_range[1]+1):
			return(i)

rand_val = 1.9669190248
ogs = []
ogi = []
ogsm =[]
c = 0  
fl = fl - 2
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy is done!':
		c+=1
		break
	if float(line.split(':')[-1]) > rand_val:
		if float(line.split(':')[-1]) in ogs:
			if line.split(',')[0] in ogsm:
				pass
			else:
				ogs.append(float(line.split(':')[-1]))
				ogsm.append(line.split(',')[0])
				it = it_ret(r_tvg,c)
				ogi.append(int(it))
		else:
			ogs.append(float(line.split(':')[-1]))
			ogsm.append(line.split(',')[0])
			it = it_ret(r_og,c)
			ogi.append(int(it))
	c +=1

#ogi is index, is then relaited to ogs


onu = []#shared smiles
for i in ogsm:
	if i in opsm:
		print(i)
		onu.append(i)



og2d = []
c = 0
for i in ogsm:
    if i in onu:
        og2d.append([ogi[c],ogs[c]])
    c+=1

og2d = np.array(og2d)

op2d = []
c = 0
for i in opsm:
    if i in onu:
        op2d.append([opi[c],ops[c]])
    c+=1    

op2d = np.array(op2d)

si , ss = [] , []
for i in op2d:
    for j in og2d:
        if all(i == j):
            si.append(i[0])
            ss.append(i[1])

#plt.scatter(opi,ops,c='#e6a157ff',label='Unique Solutions (Population)') 
#plt.scatter(ogi,ogs,c='#eb6934ff',label='Unique Solutions (Generational)') 
plt.scatter(opi,ops,label='Unique Solutions (Population)') 
plt.scatter(ogi,ogs,label='Unique Solutions (Generational)')
plt.scatter(op2d[:,0],op2d[:,1],label='Shared Solutions (Population)')
plt.scatter(og2d[:,0],og2d[:,1],label='Shared Solutions (Population)')
plt.scatter(si,ss,c='k',label='Shared Solutions') 
plt.plot([0,30],[1.9669190248,1.9669190248],linestyle='--',c='#808080ff',label='Random')
plt.xlabel('Iteration',fontsize=18)
plt.ylabel('Multi Feature Objective Score',fontsize=12)
plt.yticks(fontsize=13)
plt.xticks(range(0,31,2),fontsize=13)
#plt.title('Multi Feature Molecule Optimization',fontsize=22)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
