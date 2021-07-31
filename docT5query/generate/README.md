# docT5query/generate Folder
This folder contains the files necessary for generating queries with the docT5query model, which was created by [Nogueira and Lin](https://cs.uwaterloo.ca/~jimmylin/publications/Nogueira_Lin_2019_docTTTTTquery-v2.pdf). The model's Github repo is at https://github.com/castorini/docTTTTTquery. This implementation of docT5query uses the Huggingface Pytorch implementation. The name of the base T5 model is `t5-base` and the version that was trained by Noqueira and Lin is named `castorini/doc2query-t5-base-msmarco`.

## Folder Contents
* `genq.py`: contains the Pytorch prediction loop. It requires installation of Pytorch, the Huggingface transformers module, and nltk. 
* `doc_dataset.py`: A subclass of `torch.utils.data.IterableDataset` that feeds documents to the Pytorch prediction loop.
* `output_queries/`:  A folder containing example docT5queries that were generated from the first 1000 documents in the MSMARCO Document dataset (located in `neural_info_retrieval/test_data/msmarco-docs1000.tsv`).

## Generating Queries
### Running `genq.py`
`genq.py` is intended to be run from the command line. For example:
```bash
python genq.py \
    --num-queries 5 \
    --t5-batch-size 32 \
    --psg-min 128 \
    --psg-tgt 256 \
    --psg-max 512 \
    --output-file output_queries/t5_queries1000.tsv \
    ../../test_data/msmarco-docs1000.tsv
```
 
`genq.py` can also be imported and run from a different module, which is useful for debugging. This will bypass the argparse module's argument processing, so the user will need to pass a namespace object
with all required arguments to the `generate()` method. For example:

```python
import types

import genq

args = types.SimpleNamespace(
    num_queries=5,
    t5_batch_size=32,
    psg_min=128,
    psg_tgt=256,
    psg_max=512,
    output_file='/home/ubuntu/neural_info_retrieval/docT5query/generate/output_queries/t5_queries1000.tsv',
    path='/home/ubuntu/neural_info_retrieval/test_data/msmarco-docs1000.tsv',
    max_psg_in=None,
    qry_len=64,
    max_docs_in=None,
    doc_read_batch_size=None,
    fast_tokenizer=True)

genq.generate_queries(args)
```

### Arguments to `genq.py`
* **path**: Path to TSV file with MS Marco documents.
* **--output-file**: Path to output file. The output file will be a TSV file with three columns: Document ID, passage number (first passage is 0), and query. 
* **--psg-max**: Maximum allowed length of the input document passage that is fed to docT5query for query generation. Default is 128.
* **--psg-min**: Minimum allowed length of the input document passage that is fed to docT5query for query generation. Default is 32.
* **--psg-tgt**: Target length of input document passage. Default is 64.
* **--num-queries**: The number of queries to generate from every input passage. Default is 3.
* **--max-psg-in**: Stop generating queries after processing this many passages. Used for testing. The default is to process all passages generated from the file specified by the *path* argument.
* **--qry_len**: The max length of the generated queries. Default is 64.
* **--t5-batch-size**: The batch size for the docT5query model. Default is 32.
* **--max-docs-in**: Stop generating queries after processing this many documents. Used for testing. The default is to process all input documents. 
* **--doc-read-batch-size**: In an attempt to speed up query prediction by batching disk reads, the dataset object created by `genq.py` will read this many documents from disk at one time.
* **--fast-tokenizer**: If True, `genq.py` will use the fast (i.e., compiled) T5 tokenizer to generated queries. The default is True. Nogueira and Lin provided a custom, non-compiled tokenizer that will be used if this argument is set to False. Our brief inspection did not reveal any differences between the two tokenizer's outputs, so the default is to use the fast tokenizer. That said, we did not observe any noticeable speed-up when using the fast tokenizer.

### Notes
* The speed of query generation varies greatly depending on the input arguments, especially the number of queries generated per passage. We were unable to process more than about 30 documents per minute with this prediction loop. We estimated that generating five queries per passage for all 3.2 million documents in the MSMARCO dataset was going to take about 1,400 hours on an AWS g4dn extra large instance (has one GPU). Therefore we used a dataset of queries that Nogueira and Lin had already generated for our TRESPI model.
* The `doc_dataset.py` module uses the nltk package for splitting input documents into passages. The module attempts to split passages at sentence boundaries, to preserve context within a passage. It will add sentences to the current passage until the passage length is greater than the target passage length. Most passages will be slightly longer than the target passage length. Sentences will be split only if necessary to comply with the maximum passage length.
* `genq.py` requires the `util.indexer` and `util.log` modules.
* `genq.py` generates a logfile called `log_{datetimestamp}_train.txt`.






