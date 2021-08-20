c = 0
f = open("hyperopt_100_timed.txt","r")
x = [] 
y = []
yf = []
xf = []


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

file_name = 'hyperopt_100_timed.txt'
f =  open("hyperopt_100_timed.txt","r")

fl = file_len(file_name)
c = 0
fls = []
while c < fl:
	ll = 0
	line=f.readline()
	if line[0] != ' ':
		if line[0] != '\n':
			if len(line)>4:
				if line[3] != '%':
					fls.append(line[:-1])
	c += 1

for i in fls:
	print(i)
