from IPython.display import display, Markdown
import os.path
import sys

import pyserini.search
import pyserini.index

dirname = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(dirname, '../..'))
sys.path.insert(0, repo_root)
import util.indexer


class TrespiDemo():

    def __init__(self, index_path, docs_path, k1, b):
        self.searcher = pyserini.search.SimpleSearcher(index_path)
        self.searcher.set_bm25(k1, b)
        self.docs = util.indexer.IndexedFile(docs_path, 0)

    def run_query(self, query, num_results=100):
        hits = self.searcher.search(query, num_results)
        query_results = []
        for idx, hit in enumerate(hits):
            pos = idx + 1
            doc = self.docs[hit.docid]
            _, url, title, contents = doc.split('\t')
            result = {'pos': pos,
                      'doc_id': hit.docid,
                      'RR': 1/pos,
                      'rank': hit.score,
                      'url': url,
                      'title': title,
                      'contents': contents}
            query_results.append(result)
        return {'query': query, 'results': query_results}

    @staticmethod
    def eval_qry_results(results, relevant_docid):
        relevant_result = list(filter(lambda x: x['doc_id'] == relevant_docid,
                                 results['results']))
        if not relevant_result:
            relevant_result.append({'title': 'RELEVANT DOCUMENT NOT IN SEARCH RESULTS',
                                    'pos': 'NA',
                                    'RR': 'NA'})
        return {'query': results['query'],
                'num_results': len(results['results']),
                'relevant_docid': relevant_docid,
                'title': relevant_result[0]['title'],
                'relevant_result': relevant_result[0]}

    @staticmethod
    def print_qry_eval(qry_eval):
        print('Query:\t\t\t', qry_eval['query'])
        print('Relevant Document ID:\t', qry_eval['relevant_docid'])
        print('Document Title:\t\t', qry_eval['title'])
        print('Document Position:\t', qry_eval['relevant_result']['pos'])
        if isinstance(qry_eval['relevant_result']['RR'], float):
            print('Recipricol Rank:\t', '{:.4f}'.format(qry_eval['relevant_result']['RR']))

    @staticmethod
    def print_qry_result(results, pos, text_slice=(0, None)):
        result = results['results'][pos-1]
        print('Query:\t\t', results['query'])
        print('Document ID:\t', result['doc_id'])
        print('Position:\t', pos)
        print('Title:\t\t', result['title'])
        print('Contents:')
        print(result['contents'][text_slice[0]:text_slice[1]])
        
    @staticmethod
    def print_results(qres, tgt_doc, num_results):

        def _check_doc(doc, tgt):
            return '**' + doc + '**' if doc == tgt else doc

        results = qres['results']
        table_lines = []
        for res in results[:num_results]:
            table_lines.append(
                f"| {res['pos']} | {res['RR']:.3f} "
                f"| {_check_doc(res['doc_id'], tgt_doc)} | {res['rank']:.2f} "
                f"| {res['title'][:60]}")
        output = ('| Pos | Reciprocol Rank  | Doc.ID  | Index Rank | Title |\n' +
                  '| ----| ---------------- | ----- | ------ | ----- |\n' +
                  '\n'.join(table_lines))
        display(Markdown(output))


