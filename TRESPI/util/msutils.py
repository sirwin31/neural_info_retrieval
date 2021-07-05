import os
import os.path
import pickle
import re


class DocIndex():
    def __init__(self,
                 input_file_path='/home/ubuntu/efs/data/msmarco_docs/msmarco-docs.tsv'):
        ptn = r'\.tsv$'
        if re.search(ptn, input_file_path) is None:
            raise ValueError('Input file must end in .tsv')
        else:
            self.input_file_path = input_file_path

        self.lines = None
        self.docs = None

        # Check if index already exists
        self.index_path = re.sub(ptn, '.pickled-index', self.input_file_path)
        if not os.path.isfile(self.index_path):
            self.build_index()
            self.save_index()
        else:
            self.read_index()

        self.file = open(input_file_path, 'rt')
        

    def build_index(self):
        print('Starting to index', self.input_file_path)
        id_ptn = re.compile(r'^D\d+')
        line_index = []
        doc_index = {}
        with open(self.input_file_path, 'rt') as dfile:
            byte_pos = 0
            line_num = 0
            line = dfile.readline()
            while line != '':
                doc_id = id_ptn.match(line)[0]
                line_index.append((byte_pos, doc_id))
                if doc_id is not None:
                    doc_index[doc_id] = (byte_pos, line_num)
                byte_pos = dfile.tell()
                line_num += 1
                line = dfile.readline()
                if line_num % 500_000 == 0:
                    print(f'Lines Indexed: {line_num:>12,}')
        
        print('\nIndexing Complete.')
        print('Number of Lines:', line_num + 1)
        print(f'Number of MB: {byte_pos/1_000_000:,}')
                
        self.lines = line_index
        self.docs = doc_index

    def save_index(self):
        with open(self.index_path, 'wb')as pfile:
            pickle.dump((self.lines, self.docs), pfile)

    def read_index(self):
        print('Reading index from ', self.index_path)
        with open(self.index_path, 'rb') as pfile:
            self.lines, self.docs = pickle.load(pfile)

    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0 and key < len(self.lines):
            byte_pos = self.lines[key][0]
            self.file.seek(byte_pos)
            return self.file.readline()
        elif isinstance(key, str):
            record = self.docs.get(key, None)
            if record is not None:
                self.file.seek(record[0])
                return self.file.readline()
        raise KeyError('Key must be an integer line number or doc_id string')

    def __len__(self):
        return len(self.lines)
            
    def __del__(self):
        self.file.close()


