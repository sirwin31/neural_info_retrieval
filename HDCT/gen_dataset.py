"""Creates a datset file that maps document IDs to individual passages.

Output file is suitable for passage2doc_bert_term_sample_to_json.py
in AdeDZY/DeepCT github repo.

syntax of each output line:
{'id': docid_psg-num, 'url': document_url, 'title': document_title}

This script is intended to be run from the command line. For exmaple:
```bash
python gen_dataset.py \
    --corpus ~/msmarco_data/msmarco-queries.tsv \
    --psg-folder passages \
    msmarco_query_dataset.jsonl
```
"""

import argparse
import json
import os
import os.path
import re
import sys

from tqdm import tqdm

dirname = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(dirname, '../..'))
sys.path.insert(0, repo_root)
import util.indexer

def create_dataset(corpus, psg_folder, output):
    """Creates a JSONL dataset file for generation of HDCT term weights.

    Args:
        corpus: TSV file containing source documents. File has one
            document per line and four columns: document ID, URL, title,
            and text. The passage file name format is
            `ms-qry-passages_NNN.tsv` where NNN is three digit integer
            starting with 000 that identifies the file order.
        psg_folder: Folder that contains passage text files. Passage
            files are TSV files with two columns: {doc ID}_{passage #},
            and the text passage. The 
        output: Path to output file, which will be a JSONL file with
            one dictionary per line. Dictionary has keys id, url, and
            title.
    """
    corpus = os.path.abspath(corpus)
    psg_folder = os.path.abspath(psg_folder)

    doc_idx = util.indexer.IndexedFile(corpus, 0)
    ptn = re.compile(r'D\d+')
    print('Writing output to', output)
    with open(output, 'wt') as ofile:
        for psg_id in tqdm(row_iter(psg_folder), 'Docs Processed'):
            doc_id = re.match(ptn, psg_id)[0]
            _, url, title, _ = doc_idx[doc_id].split('\t')
            output_dict = {'id': psg_id, 'url': url, 'title': title}
            output_str = json.dumps(output_dict) + '\n'
            ofile.write(output_str)


def row_iter(psg_folder):
    """Iterates over passage files, returning a single line at a time."""
    input_files = ['ms-qry-passages_{:03}.tsv'.format(idx)
                   for idx in range(33)]
    input_paths = [os.path.join(psg_folder, input_file)
                    for input_file in input_files]
    for input_path in input_paths:
        with open(input_path) as ifile:
            for line in ifile:
                yield line.split('\t')[0]


if __name__ == '__main__':
    desc = ('Creates dataset file that is required for generating HDCT terms. '
            'Passage file name format: `ms-qry-passages_NNN.tsv` where '
            'NNN is three digit integer starting with 000 that identifies '
            'the file order.')
    parser = argparse.ArgumentParser(desc)
    parser.add_argument('--corpus', required=True,
                        help='TSV file that contains the source documents.')
    parser.add_argument('--psg-folder', required=True,
                        help='Path to folder containing passage files.')
    parser.add_argument('OUTPUT', help='Name of output dataset file.')
    args = parser.parse_args()
    create_dataset(args.corpus, args.psg_folder, args.OUTPUT)
