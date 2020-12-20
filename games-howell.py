from collections import defaultdict

d = defaultdict(list)
all = []

with open(filepath) as f:
    for line in f:
        if line.strip():
            k,v,p = map(float,line.split(","))
            if (p > 0.9):
             if v not in all or k not in all: 
                 d[k].append(v)
                 all.append (v)
for key,values in d.items():
 if values:
  print(key, values)


l = [ [k]+v for k,v in d.items()]

