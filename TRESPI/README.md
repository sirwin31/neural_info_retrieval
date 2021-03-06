# Combining Indexes with TRESPI

The module `TRESPI.joiner` contains a class called `IndexJoiner` that can
combine two different indexes using various techniques.

## Example Code for Joining Indexes
```python
import combine_indexes.joiner as joiner

idx1_path ='~/idx1'
idx2_path ='~/idx2'

out_path = '~/joined_idx'

jnr = joiner.IndexJoiner([idx1_path, idx2_path])

jnr.set_join_type('join_docs_max_weights_qry_discount',
                  {'qry_discount': 0.8})

jnr.join_indexes(out_path)
```

idx1_path and idx2_path are paths to two different document indexes
generated by the HDCT model. Each path can contain several JSONL
files, where each line is a JSON dictionary:
```python
{'id'; 'contents': 'word0 word0 word1 word2 word2 word2 ... wordN'}
```
The JSONL files are formatted such that they can be read by the
Lucene index generator. Term weights are encoded per the number of
repetitions of each word. If a word has a term weight of 10, for example,
the word will be repeated 10 times, separated by spaces.

The document indexes need not list documents in the same order.
If a document appears in one index but not the other index, the
document will generally be included in the final index, depending
on the specific join method.

Initializing IndexJoiner does NOT join the indexes. Joining indexes
requires two additional method calls.

1. IndexJoiner.set_join_type(join_type, join_args)
    * `join_type` is a string that matches the name of one of the
    join methods. The currently available join methods are:
        * join_docs_sum_weights
        * join_docs_avg_weights_qry_discount
        * join_docs_max_weights_qry_discount
    * `join_args` is a dictionary containing the custom arguments
    needed for the join. The key is the name of the argument.
    For example, join_docs_avg_weights_qry_discount requires one
    additional argument, 'qry_discount'. For this join type, the
    join_args argument should be `{'qry_discount': F} where F is
    a floating point number.
2. IndexJoiner.join_indexes(output_path)
    * output_path is a path to an empty folder. The joined index
    files will be written to this folder. The folder must already
    exist before calling `join_indexes`.

When joining indexes, IndexJoiner iterates through every entry in
index 0 and retrieves the corresponding record from index 1 using
the index datastructure contained in util.indexer.IndexedFile.
The records for the two indexes need not be in the same order.
Also, if one index is larger than the other, recommend that index
be procssed as index 0.

Initializing an IndexJoiner object results in the creation of
sevaral data files.
1. a *.pickled-index file is created for each input file. The
*.pickled-index files contain indexes to every document ID in all
input files, allowing fast random access to document term weights
given a document ID. These files will be created from scratch the
first time IndexJoiner is initialzied on a given set of input files,
but for subsequent runs, the indexes need only be read from disk,
which is much faster. The *.pickled-index files are generated by
the util.indexer.IndexedFile class.
2. When first initialized, IndexJoiner identifies all mismatched
document IDs. Mismatched document IDs are ID values that appear in
only one of the input indexes, but not both. For large indexes, this
step is time consuming. The mismatched document IDs are written to
the file specified by the constructor's `join_data_file` argument.
If the file alredy exists, the mismatched document IDs are read from
the file instead of being recalculated, which saves considerable
time. Be careful not use an old join data file calculated from
different document indexes.