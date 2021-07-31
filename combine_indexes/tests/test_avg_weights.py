import json
from json.decoder import JSONDecodeError
import os.path

from tqdm import tqdm

import combine_indexes.joiner as joiner

def test_avg_weights():
    doc_path ='/home/ubuntu/efs/combined_index_18Jul/docs_spl'
    qry_path ='/home/ubuntu/efs/combined_index_18Jul/queries_spl'
    out_path = '/home/ubuntu/efs/stacy/neural_info_retrieval/combine_indexes/joined_idx'

    jnr = joiner.IndexJoiner([doc_path, qry_path])
    jnr.set_join_type('join_docs_avg_weights_qry_discount',
                      {'qry_discount': 0.5})
    jnr.join_indexes(out_path)



    with open(os.path.join(out_path, 'docs00.json')) as jfile:
        for doc_txt in tqdm(jfile):
            docj = json.loads(doc_txt)
            try:
                doc0 = json.loads(jnr.get_doc(0, docj['id']))
                doc1 = json.loads(jnr.get_doc(1, docj['id']))
            except JSONDecodeError:
                continue

            assert docj['id'] == doc0['id']
            assert doc0['id'] == doc1['id']

            doc0_weights = jnr._get_weights(doc0)
            doc1_weights = jnr._get_weights(doc1)

            compare_data = jnr._compare_terms(doc0_weights, doc1_weights)

            jnr.join_args = {'qry_discount': 0.5}
            avg_term_data = jnr.join_docs_avg_weights_qry_discount(doc0, doc1)
            avg_term_weights = jnr._get_weights(avg_term_data)

            for term in compare_data['doc0_only_terms']:
                assert avg_term_weights['weights'][term] == doc0_weights['weights'][term]
                assert term not in doc1_weights['weights'].keys()

            for term in compare_data['doc1_only_terms']:
                discounted_weight = round(doc1_weights['weights'][term] * 0.5)
                assert avg_term_weights['weights'][term] == int(max(discounted_weight, 1))
                assert term not in doc0_weights['weights'].keys()

            for term in compare_data['common_terms']:
                qry_discount = jnr.join_args['qry_discount']
                doc0_wt = doc0_weights['weights'][term]
                doc1_wt = doc1_weights['weights'][term]
                doc1_wt_disc = qry_discount * doc1_weights['weights'][term]
                avg_weight = round((doc0_wt + doc1_wt_disc) / 2)
                assert avg_term_weights['weights'][term] == int(max(avg_weight, 1))    