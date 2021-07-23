import json
import os.path
import sys

# Run test from util directory
sys.path.insert(0, os.path.abspath('.'))
import indexer

def test_json():
    fpath = os.path.abspath('docs00.json')
    didx = indexer.IndexedFile(fpath, 'id')
    assert didx.input_file_path == fpath
    assert len(didx) == 1000
    id1 = 'D2963174'
    line_data = json.loads(didx[id1])
    assert line_data['id'] == id1
    assert line_data['contents'][:8] == 'exercise'
    didx.close()

def test_tsv():
    fpath = os.path.abspath(('docs00.tsv'))
    didx = indexer.IndexedFile(fpath, 0)
    assert didx.input_file_path == fpath
    assert len(didx) == 1000

    id1 = 'D3502052'
    line = didx[id1]
    line_data = line.split('\t')
    assert line_data[0] == id1
    assert line_data[1] == r'http://www.legal500.com/c/france'
    didx.close()
