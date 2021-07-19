"""Creates msmarco documents based on docT5query queries.

This module relies on a sequence of three different iterators and
several helper functions.

Iterators:
* _read_queries_from_files(): This function iterates over all 330
  docT5query data files to extract the queries that correspond to a
  given passage. It returns a list of queries. Note there are usually
  multiple passages per document.
* _get_docids(): Iterates over the docT5query dataset's passage to
  doc_id mapping file. It returns the msmarco docuemnt ID that
  corresponds to a passage.
* _get_doc_queries(): Using the output of the two preceding iterators,
  provides a tuple consisting of a document ID and a list of all queries
  that correspond to the document.

Primary Function:
create_query_docs(): Creates a TSV document with four columns:
* doc_id
* document URL
* document title
* document queries, concatenated into a single string with queries
  separated by spaces.

Helper Functions:
* _close_files(): Closes all data files.
* _clean_queries(): Strips surrounding whitespace and ensures each query
  ends with a '?'.
"""

import argparse
import os.path
import sys

from tqdm import tqdm

HOME_PATH = '/home/ubuntu/efs/query_termweights_14Jul'
sys.path.append(HOME_PATH)
import util.msutils



HOME_PATH = '/home/ubuntu/efs/query_termweights_14Jul'
QUERIES_PATH = os.path.join(HOME_PATH, 'dT5_queries/predicted')
DOCIDS_PATH = os.path.join(HOME_PATH, 'dT5_queries/msmarco_doc_passage_ids.txt')
DOCS_PATH = '/home/ubuntu/efs/data/msmarco_docs/msmarco-docs.tsv'
OUTPUT_PATH = os.path.join(HOME_PATH, 'dT5_queries/msmarco-queries.tsv')


# Helper Functions
def _close_files(files):
    """Takes a list of file objects and closes each file"""
    for f in files:
        if not f.closed:
            f.close()

def _clean_queries(queries):
    """Strips whitespace and ensures each query ends with a '?'."""
    queries = [query.strip() for query in queries]
    queries = [query + '?' if query[-1] not in ['.', '!', '?'] else query
            for query in queries]
    return queries


# Iterators
def _read_queries_from_files(queries_per_psg):
    """An iterator that reads queries from docT5query files.

    Args:
        queries_per_psg: Number of queries to obtain for each
            passage.

    Returns: A list of queries, with the length of each list being equal
    to `queries_per_psg`. Each list corresponds to a different passage
    within an msmarco document. Example return value for
    queries_per_psg = 3:
    ```
    ['when find radius of star r',
    'which radiation is produced during a solar radiation experiment?'
    'which age are kids learning how to be independent?']
    ```
    The queries are returned in the order in which they occur in the
    source data files.
    
    There are usually several passages within an msmarco document, so it
    is necessary to call this iterator multiple times to get all queries
    for a single document.

    This is the only part of the module that accesses the docT5query
    data files. The structure of these files is confusing, so it is
    described in the following section to make future code maintenance
    easier.

    Data File Description:
    ----------------------
    There are 330 data files that contain the docT5queries. In total,
    there are 10 queries for every msmarco document passage. The format
    of the file names is:
    predicted_queries_doc_sampleQQQ.txtFFF-1004000, where QQQ denotes
    the query number for a given passage, and FFF denotes a file
    sequence number. QQQ ranges from 000 to 009 and FFF ranges from
    000 to 032.

    If we wanted one query per passage, we would iterate through 33
    files: predicted_queries_doc_sample000.txt000-1004000 to 
    predicted_queries_doc_sample000.txt033-1004000. Each file contains
    one query per passage, with one query per line. Since there are
    over 20,000,000 passages, the data is split into 33 differrent
    files, with the order of the files denoted by .txtFFF.

    If we want two queries per passage, we need to iterate over two
    sequences of 33 files each, or 66 files. The two sequences are:
    * predicted_queries_doc_sample000.txt000-1004000 to 
      predicted_queries_doc_sample000.txt033-1004000
    * predicted_queries_doc_sample001.txt000-1004000 to 
      predicted_queries_doc_sample001.txt033-1004000

    The two sequences are in the same order, so if we want to aggregate
    queries for the same passage, we need to iterate over the sequences
    in parallel.
    """
    try:
        for file_num in range(33):
            # Each file has one query per passage. Open one file for
            #   each query that will be returned.
            query_file_names = [
                f'predicted_queries_doc_sample{qnum:03}'
                f'.txt{file_num:03}-1004000'
                for qnum in range(queries_per_psg)]
            print('Reading files:', query_file_names)
            query_files = [open(os.path.join(QUERIES_PATH, qf_name))
                        for qf_name in query_file_names]
            while True:
                # Read a query from each open file
                psg_queries = [qfile.readline() for qfile in query_files]
                if not psg_queries[0]:  # readline returns '' at EOF
                    break
                yield psg_queries
    # Close files if iterator is closed early
    except GeneratorExit:
        _close_files(query_files)
    _close_files(query_files)

def _get_docids():
    """Iterates over the docT5query passage to doc_id mapping file.

    Returns a doc_id string.
    """
    with open(DOCIDS_PATH) as idfile:
        for line in idfile:
            yield line.strip()

def _get_doc_queries(queries_per_psg, max_docs=0):
    """Returns a doc_id and a list of all queries for the document.

    Args:
        queries_per_psg: Number of queries to obtain for each
            passage.
        max_docs: Number of documents to process. The iterator will
            be exhausted after this number of documents. If 0, all
            documents are processed.

    Returns:
        (doc_id, [qry_1, qry_2, qry_3, ... qry_m])
        m = queries_per_psg * {number of passages in document}
        Documents contain varying numbers of passages, so the list of
        queries will have varying lengths.
    """
    curr_docid = ''
    doc_num = 0  # For tracking number of documents processed
    for doc_id, query_list in zip(_get_docids(),
                                  _read_queries_from_files(queries_per_psg)):
        if doc_id != curr_docid:
            if curr_docid:
                yield (curr_docid, [qry for qlist in queries for qry in qlist])
                doc_num += 1
                # Stop if max_docs is reached
                if max_docs and doc_num >= max_docs:
                    return
            queries = [query_list]
            curr_docid = doc_id
        else:
            queries.append(query_list)
    # Make sure the final document is returned.
    yield (curr_docid, [qry for qlist in queries for qry in qlist])


# Primary Function
def create_query_docs(queries_per_psg=1, max_docs=0):
    """Creates a TSV file containing queries from docT5query.

    The results are written to the file specified by OUTPUT_PATH

    Args:
        queries_per_psg: Number of queries to obtain for each
            passage.
        max_docs: Number of documents to process. The iterator will
            be exhausted after this number of documents. If None, all
            documents are processed.

    Returns: None
    """
    doc_idx = util.msutils.DocIndex(DOCS_PATH)
    total_docs = len(doc_idx)
    if max_docs is not None:
        docs_to_process = min(total_docs, max_docs)
    else:
        docs_to_process = total_docs
    print('Writing output to', OUTPUT_PATH)
    with open(OUTPUT_PATH, 'wt') as ofile:
        for doc_id, qset in tqdm(_get_doc_queries(queries_per_psg, max_docs),
                                'Docs Processed', docs_to_process):
            _, url, title, text = doc_idx[doc_id].split('\t')
            query_txt = ' '.join(_clean_queries(qset))
            output = '\t'.join([doc_id, url, title, query_txt]) + '\n'
            ofile.write(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Creates msmarco documents based on docT5query queries.')
    parser.add_argument('--queries-per-psg', type=int, default=10)
    parser.add_argument('--max-docs', type=int, default=0)
    args = parser.parse_args()

    create_query_docs(args.queries_per_psg, args.max_docs)

