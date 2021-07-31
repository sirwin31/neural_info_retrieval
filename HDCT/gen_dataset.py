"""Creates a datset file that maps document IDs to individual
passages. Output file is suitable for passage2doc_bert_term_sample_to_json.py
in AdeDZY/DeepCT github repo.

syntax of each output line:
{'id': docid_psg-num, 'url': document_url, 'title': document_title}
"""

import json
import os
import os.path
import re
import sys

from tqdm import tqdm

sys.path.append('..')
import util.msutils

PSG_FILES = '/home/ubuntu/efs/query_termweights_14Jul/dT5_passages'
CORPUS = '/home/ubuntu/efs/query_termweights_14Jul/dT5_queries/msmarco-queries.tsv'
OUT_FILE = '/home/ubuntu/efs/query_termweights_14Jul/msmarco_query_dataset.jsonl'

NUM_LINES = 9_541_725

doc_idx = util.msutils.DocIndex(CORPUS)

def create_dataset():
    ptn = re.compile(r'D\d+')
    print('Writing output to', OUT_FILE)
    with open(OUT_FILE, 'wt') as ofile:
        for psg_id in tqdm(row_iter(), 'Docs Processed',NUM_LINES):
            doc_id = re.match(ptn, psg_id)[0]
            _, url, title, _ = doc_idx[doc_id].split('\t')
            output_dict = {'id': psg_id, 'url': url, 'title': title}
            output_str = json.dumps(output_dict) + '\n'
            ofile.write(output_str)


def row_iter():
    input_files = ['ms-qry-passages_{:03}.tsv'.format(idx)
                   for idx in range(33)]
    input_paths = [os.path.join(PSG_FILES, input_file)
                    for input_file in input_files]
    for input_path in input_paths:
        with open(input_path) as ifile:
            for line in ifile:
                yield line.split('\t')[0]



if __name__ == '__main__':
    create_dataset()
