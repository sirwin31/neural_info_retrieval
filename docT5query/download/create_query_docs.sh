python create_query_docs.py \
    --queries-folder ~/efs/dt5/queries \
    --queries-per-psg 5 \
    --msmarco-docs-path ~/efs/data/msmarco_docs/msmarco-docs.tsv \
    --doc-ids-path ~/efs/dt5/msmarco_doc_passage_ids.txt \
    --output-path msmarco_queries.txt