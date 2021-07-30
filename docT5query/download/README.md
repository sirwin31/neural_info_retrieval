# Create Document Dataset from Queries Generated by docT5query
Nogueira et. al. provided a dataset consisting of queries generated by
their docT5query model from the MSMARCO document dataset. The
`create_query_docs.py` script converts these queries into a document
dataset contained within a TSV file. The file is formatted identically
to the msmarco-docs.tsv file from the MSMARCO document dataset, except
that instead of containing the document's text, it contains the queries
generated by the docT5query model.

## Obtaining the MSMARCO Document docT5query Dataset
A link to the docT5query MSMARCO document dataset is provided on the
[docT5query Github repository.](https://github.com/castorini/docTTTTTquery)
The dataset consistes of two files:
* The queries are contained in the file `predicted_queries_doc.tar.gz`.
* The `msmarco_doc_passage_ids.txt` maps queries to MSMARCO document IDs.

## DocT5query Dataset Structure
The `predicted_queries_doc.tar.gz` decompresses to 330 text files. Each
file name has the syntax predicted_queries_doc_sampleQQQ.txtFFF-1004000
where QQQ is the query sample number relative to a given passage and FFF
denotes a file sequence number. There are ten queries per passage,
therefore QQQ ranges from 000 to 009. There are 33 files for each
query sample number, therefore FFF ranges from 000 to 032.

For example, if we only needed one query per passage, we would iterate
through 33 files: predicted_queries_doc_sample000.txt000-1004000 to 
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

## Running `create_query_docs.py`
The `create_query_docs.py` script will create an index for the MSMARCO
documents file and store this index in in a file in the same folder.
The index is created using the `util.indexer.IndexedFile`. Consequently
write access is required for the folder that contains the MSMARCO
documents file.

`create_query_docs.py` uses a relative import to for the
`util.indexer.IndexedFile` class. It must be run from the
*create_query_docs* folder for the import to work correctly.

### Example
```bash
python create_query_docs.py \
    --queries-folder ../../dt5/queries \
    --queries-per-psg 5 \
    --msmarco-docs-path ../../data/msmarco_docs/msmarco-docs.tsv \
    --doc-ids-path ../../dt5/msmarco_doc_passage_ids.txt \
    --output-path msmarco_queries.tsv
```