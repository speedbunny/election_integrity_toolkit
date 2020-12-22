filepath = '/users/apple/Datasets/PA/PAt.txt'

#Import Default Dict
from collections import defaultdict

#Declare dictionary and all
d = defaultdict(list)
all = []

#Read file line by line for each line
with open(filepath) as f:
    for line in f:
        if line.strip():
        #Create three variables
            k,v,p = map(float,line.split(","))
            #If p is 1
            if (p == 1):
            #Uncomment to just return single pairs
             #if v not in all or k not in all: 
             #Add value v to dictionary with key k
                 d[k].append(v)
              #   all.append (k)
              #   all.append (k)
for key,values in d.items():
 if values:
  print(key, values)
