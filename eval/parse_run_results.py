
# finetune-4.5-0.2.out

#Quantity of Documents ranked for each query is as expected. Evaluating
#####################
#MRR @100: 0.279924693277269
#QueriesRanked: 5193
######################


import glob
import re
import pandas as pd

file_list = glob.glob("*.out")
results = []
for file in file_list:
    body = open(file,'r').read()
    file = file.replace('finetune-','').replace('.out','')
    (k1,b) = file.split('-',2)
    mrr = re.search('MRR @100: (.+)\n',body)[1]
    results.append((float(k1),float(b),float(mrr)))
results.sort(key=lambda x: x[2])
pd.DataFrame(results,columns=['k1','b','mrr']).to_csv('results.txt')

