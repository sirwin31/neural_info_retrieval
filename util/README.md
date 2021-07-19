# Utility Modules
## indexer.py
The IndexedFile builds an index for a JSONL, TSV, or other delimited
file. Once the index is built, any record can be quickly accessed  with
it's unique key value. The index is saved to disk after it is created.
The indexe's file name is the the source file name with 'pickled-index'
added to the end.

IndexedFile assumes that there is a unique key value for every line in
the file. For JSONL files, each line must be a dictionary object.

Typical Usage Example:
```python
import util.indexer

doc_idx = indexer.IndexedFile('docs00.tsv', 0)
record = doc_idx['D3502052']
```

## log.py
Returns a Python Standard Library logger object that logs messages to a
file and the console.

Useage Example:
```python
import sys
sys.path.insert(0, '/home/jupyter')
import util.log
logger = util.log.get('log_name')
logger.info('Dislay info message.')
logger.warning('Oh-oh, something fishy is going on')
```
All information sent to logger will be displayed.
All messages prefixed with a time_date stamp of format "%H%M_%Y%m%d".