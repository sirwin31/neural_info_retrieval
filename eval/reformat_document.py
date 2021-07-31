import sys


input_file = sys.argv[1]

with open(input_file,"r") as fh:
    for entry in fh:
        a,b,c,d,e,f = entry.rstrip().split(' ',6)
        c = c.replace('D','')
        print("{} {} {} {} {} {}".format(a,b,c,d,e,f))

