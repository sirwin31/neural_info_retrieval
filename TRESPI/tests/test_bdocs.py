import sys

sys.path.append('..')

import batched_dataset

DOC_PATH = '/home/ubuntu/efs/data/msmarco_docs/msmarco-docs.tsv'
TEST_DOCS_PATH = '/home/ubuntu/neural_info_retrieval/TRESPI/tests/test-ms-docs.tsv'

class TestBatchedDataset:

    def test_batch_dataset(self):
        bdset = batched_dataset.DocDataset(TEST_DOCS_PATH, doc_batch_size=3)
        assert len(bdset.doc_idx) == 10
        doc_iter = iter(bdset)
        # for doc in doc_iter:
        #     print(doc)
        print(next(doc_iter))
    
