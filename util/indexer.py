"""A tool for creating an index into a TSV or JSONL text file.

The IndexedFile builds an index for a JSONL, TSV, or other delimited
file. Once the index is built, any record can be quickly accessed  with
it's unique key value. The index is saved to disk after it is created.
The indexes file name is the the source file name with 'pickled-index'
added to the end.

IndexedFile assumes that there is a unique key value for every line in
the file. For JSONL files, each line must be a dictionary object.

Typical Usage Example:
import indexer
doc_idx = indexer.IndexedFile('big_doc.tsv', 0)
record = doc_idx['key-value']
"""

import json
import os
import os.path
import pickle

class IndexedFile():
    """Represents an indexed JSONL, TSV, or other delimited file.

    Constructor arguments:
        input_file_path: The absolute path to the JSONL, TSV or other
            delimited text file.
        key_idx: Specifies the location of the key value within each
             line of the source text file. For delimited files like TSV
             or CSV, key shoudl be an integer that identifies the
             position of the column that contains the key, starting at 0
             for the leftmost column. For JSONL files, key should be a
             string containing the dictionary key that contains the
             unique key value (i.e., record identifier)
        delim: The character or string that separates columns within a
            delimited file. Optional, defaults to '\t'.
        line_idx: If True, records will be retrievable by line number,
            in addition to being retrieved by the key value. Defaults to
            False because indexing by lines as well as key values
            significantly increases the size of the index file.

    Attributes:
        close(): IndexedFile keeps the source file open for quick data
            access. This method will close the source file. No data will
            be accessible after calling close(). The file will also be
            closed if the IndexedFile object is deleted.

    Examples:
    idx_file = indexer.IndexedFile('big_file.json', 'id')
    # Get number of records in file
    num_records = len(idx_file)
    # Get line from file for a specifi key value:
    line_txt = idx_file['id3527']
    # Done with IndexedFile
    idx_file.close()
    """
    def __init__(self, input_file_path, key_idx, delim='\t', line_idx=False):
        """Creates index or reads index from disk."""
        # Check arguments
        if not os.path.isfile(input_file_path):
            raise ValueError('Input file "{}" does not exist.'
                             .format(input_file_path))
        self.input_file_path = input_file_path

        error_msg = 'Key index must be a non-negative integer or string.'
        if not isinstance(key_idx, (str, int)):
            raise ValueError(error_msg)
        if isinstance(key_idx, int) and key_idx < 0:
            raise ValueError(error_msg)
        self.key_idx = key_idx
        self.delim = delim
        self.line_idx = line_idx
        self.lines = None
        self.docs = None

        # Check if index already exists - if not, build index
        self.index_path = self.input_file_path + '.pickled-index'
        if not os.path.isfile(self.index_path):
            self._build_index()
            self._save_index()
        else:
            self._read_index()

        # Open indexed document for access
        self.file = open(input_file_path, 'rt')
        
    def _build_index(self):
        """Builds a new index if index does not already exist."""
        print('Starting to index', self.input_file_path)
        line_index = []
        doc_index = {}
        with open(self.input_file_path, 'rt') as dfile:
            byte_pos = 0
            line_num = 0
            line = dfile.readline()
            while line != '':
                key = self._get_key(line)
                line_index.append((byte_pos, key))
                if key is not None:
                    doc_index[key] = (byte_pos, line_num)
                byte_pos = dfile.tell()
                line_num += 1
                line = dfile.readline()
                if line_num % 500_000 == 0:
                    print(f'Lines Indexed: {line_num:>12,}')
        
        print('\nIndexing Complete.')
        print('Number of Lines:', line_num + 1)
        print(f'Number of MB: {byte_pos/1_000_000:,}')
        
        if self.line_idx:
            self.lines = line_index
        self.docs = doc_index

    def _get_key(self, line):
        """Gets unique key value from line in text file."""
        if isinstance(self.key_idx, int):
            # Source file is TSV, CSV, or similar and key is in key-th col
            return line.split(self.delim)[self.key_idx]
        else:
            # Source file is JSONL and key value has dictionary key = key_idx
            return json.loads(line)[self.key_idx]

    def _save_index(self):
        """Saves index data structure to disk as a pickle file."""
        with open(self.index_path, 'wb')as pfile:
            pickle.dump((self.docs, self.lines), pfile)

    def _read_index(self):
        """Reads index datastructure from disk."""
        print('Reading index from ', self.index_path)
        with open(self.index_path, 'rb') as pfile:
            self.docs, self.lines = pickle.load(pfile)

    def __getitem__(self, key):
        """Allows array-style line access, using key value or line #."""
        if isinstance(key, str):
            idx_record = self.docs.get(key, None)
            if idx_record is not None:
                self.file.seek(idx_record[0])
                return self.file.readline()
            else:
                error_msg = ('Key {} does not exist in index.'
                             .format(key))
                raise KeyError(error_msg)
        if isinstance(key, int):
            if self.lines is None:
                error_msg = 'Integer key provided but line index not available.'
                raise KeyError(error_msg)
            elif key >= 0 and key < len(self.lines):
                byte_pos = self.lines[key][0]
                self.file.seek(byte_pos)
                return self.file.readline()
            else:
                error_msg = ('Integer key {} out of range.'.format(key))
        raise KeyError('Key must be an integer line number or string')

    def __len__(self):
        """Gets number of records in index."""
        return len(self.docs)
    
    def close(self):
        """Close source text file if finished with data access."""
        self.file.close()

    def __del__(self):
        """Close source text file if IndexedFile object is deleted."""
        self.file.close()