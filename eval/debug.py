import numpy as np

# wade.holmes@berkeley.edu
# objective here is to debug why our MRR is so low
# script output piped to output text for analysis
# root cause on low MRR is that many documents are not in the top 100, or low rank

fh = open('src/main/resources/topics-and-qrels/qrels.msmarco-doc.dev.txt','r')
for line in fh.readlines():
    (query,j1,document,j2) = line.rstrip().split('\t')

    fh2 = open('/home/ubuntu/efs/msmarco_leaderboard_attempt9/runs/run.msmarco-doc.leaderboard-dev.bm25base.txt','r')
    resultmap = {'query': query, 'best_document': document, 'matches': 0, 'rr': [], 'mrr': 0}
    for line2 in fh2.readlines():
        (tquery,tdoc,rank) = line2.rstrip().split('\t')

        if document == tdoc:
            resultmap['matches'] += 1
            resultmap['rr'].append(rank)

    # find the result
    resultmap['mrr'] = np.mean([ 1/int(x) for x in resultmap['rr']])
    print(resultmap)

