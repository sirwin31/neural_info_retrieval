import sys

import pytest
import torch.utils.data

sys.path.append('/home/ubuntu/TRESPI')

import doc_dataset as ds

TEST_DOCS = '/home/ubuntu/TRESPI/tests/test-ms-docs.tsv'

class TestDataset:

    docids = set(['D1555982', 'D301595', 'D1359209', 'D2147834',
              'D1568809', 'D3233725', 'D1150618', 'D1885729',
              'D1311240', 'D3048094'])

    def test_dataset(self):
        dset = iter(ds.DocDataset(TEST_DOCS))
        for passage in dset:
            assert isinstance(passage, tuple)
            docid = passage[0]
            assert isinstance(docid, str)
            assert docid in self.docids
            assert isinstance(passage[1], int)
            assert isinstance(passage[2], list)
            assert isinstance(passage[3], list)
            assert len(passage[2]) == 512
            assert len(passage[3]) == 512

        dset.close()

    def test_dataloader(self):

        dataset = ds.DocDataset(TEST_DOCS)
        docloader = torch.utils.data.DataLoader(
            dataset,
            batch_size=10,
            shuffle=False
        )

        for batch in docloader:
            print(batch[0], batch[2])
        
        dataset.close()

