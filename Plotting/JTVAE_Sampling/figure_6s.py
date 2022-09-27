#### plotter for figure 6a# needs to be python2 to handle pickles generated in python2 (JTVAE)

##traversky pop
import numpy as np
import matplotlib
matplotlib.rcParams['axes.spines.right'] = False
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.linewidth'] = 1.5
matplotlib.use('Agg')
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
	for j in range(gen_range[0],gen_range[1]+1):
			temp.append(runner.seed_fitness[j])
	tv_p.append(sum(temp)/(len(temp)+0.0))
	tv_p_b.append(max(temp))



r_tvg= paddy.utils.paddy_recover('Paddy_Tversky_Gen_2')
tv_g = []
tv_g_b =[]
for i in range(0,29):
	gen_range=r_tvg.generation_data[str(i)]
	temp = []
	for j in range(gen_range[0],gen_range[1]+1):
			temp.append(r_tvg.seed_fitness[j])
	tv_g.append(sum(temp)/(len(temp)+0.0))
	tv_g_b.append(max(temp))

plt.figure()
plt.plot(range(0,31),tv_p,c='#4275A7',linestyle='--',label='Iteration Average (Population)')
plt.plot(range(0,31),tv_p_b,c='#4275A7',label='Best in Iteration (Population)')
plt.plot(range(0,29),tv_g,c='#B52F3A',linestyle='--',label='Iteration Average (Generational)')
plt.plot(range(0,29),tv_g_b,c='#B52F3A',label='Best in Iteration (Generational)')
plt.plot([0,30],[0.669344042838,0.669344042838],linestyle='--',c='#808080ff',label='Random')
plt.xlabel('Iteration',fontsize=18)
plt.ylabel('Tversky Similarity',fontsize=18)
plt.yticks(fontsize=13)
plt.xticks(range(0,31,2),fontsize=13)
#plt.title('Multi Feature Molecule Optimization',fontsize=22)
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig(fname='vae_a_s.svg',dpi=600)
plt.show()

####Figure 6c#### done without correct collors
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


r_tvg= paddy.utils.paddy_recover('Paddy_Tversky_Gen_2')
file_name = 'Paddy_Tversky_Gen_2.txt'
f = open("Paddy_Tversky_Gen_2.txt","r")


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
tg_dic = {}
c = 0
fl = fl -2  
while c < fl:
	line = f.readline().strip()
	if line == '':
		break
	if line == 'paddy has converged':
		c+=1
		break        
	if float(line.split(':')[-1]) > rand_val:
		if float(line.split(':')[-1]) in tvgs:
			if line.split(',')[0] in tvgsm:
				tg_dic[line.split(',')[0]][1] += 1
				pass
			else:
				tvgs.append(float(line.split(':')[-1]))
				tvgsm.append(line.split(',')[0])
				tg_dic[tvgsm[-1]] = [tvgs[-1],1]
				it = it_ret(r_tvg,c)
				tvgi.append(int(it))
		else:
			tvgs.append(float(line.split(':')[-1]))
			tvgsm.append(line.split(',')[0])
			tg_dic[tvgsm[-1]] = [tvgs[-1],1]
			it = it_ret(r_tvg,c)
			tvgi.append(int(it))
	c +=1

print("tg dic")
print(tg_dic)

plt.figure()
plt.scatter(tvpi,tvps,c="#4275A7",label='Unique Solutions (Population)') 
plt.scatter(tvgi,tvgs,c="#B52F3A",label='Unique Solutions (Generational)') 
plt.plot([0,30],[0.669344042838,0.669344042838],linestyle='--',c='#808080ff',label='Random')
plt.xlabel('Iteration',fontsize=18)
plt.ylabel('Tversky Similarity',fontsize=18)
plt.yticks(np.arange(0.65,0.85,.05),fontsize=13)
plt.xticks(range(0,31,2),fontsize=13)
#plt.title('Tversky Similarity Optimization',fontsize=22)
plt.legend(loc='lower right',fontsize=12)
plt.tight_layout()
plt.savefig(fname='vae_c_s.svg',dpi=600)
plt.show()

print(tvgs)

