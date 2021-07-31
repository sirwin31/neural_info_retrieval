import sys


input_file = sys.argv[1]

with open(input_file,"r") as fh:
    for entry in fh:
        doc1,doc2,val = entry.rstrip().split('\t',3)
        doc2 = doc2.replace('D','')
        print("{}\t{}\t{}".format(doc1,doc2,val))

