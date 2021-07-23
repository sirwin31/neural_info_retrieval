import os
import os.path
import sys

sys.path.append('/home/ubuntu/neural_info_retrieval/TRESPI')

import docdex

class TestDocRetrieve():
    # def test_path(self):
    #     print(docdex.__dir__)
    #     print(sys.path)
    #     print(os.listdir('/home/ubuntu/neural_info_retrieval/TRESPI'))

    def test_init(self):
        input_path = '/home/ubuntu/neural_info_retrieval/TRESPI/test-docs.tsv'
        didx = docdex.MSDocIndex(input_path)
        assert didx.input_file_path == input_path
        assert didx.index_path == input_path[:-4] + '.pickled-index'