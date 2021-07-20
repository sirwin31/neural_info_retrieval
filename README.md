# neural_info_retrieval
Summer 2021 capstone project for Wang, Khural, Irwin, and Holmes

## Workflow
### 1. Generate Dataset from DocT5query
Nogueira et. al. generated 10 queries for every document in the MSMarco
document data set and made these queries available online. We aggregated
the queries for each document into a dataset nearly identical to the
MSMARCO dataset. They query dataset contains the MSMARCO document ID, URL,
and title. The only difference is that the original text has been replaced
with the queries generated by docT5query. The pthon code that generated
the query dataset is in the
[create_qeury_docs folder.](https://github.com/sirwin31/neural_info_retrieval/tree/main/create_query_docs)

### 2. Split Documents into Passages
The documents from both the MSMARCO document and the query documents must be
split into individual passages before they can be submitted to the
DeepCT prediction step. Tools and guidance are in the
[doc_split_deepCT folder](https://github.com/sirwin31/neural_info_retrieval/tree/main/doc_split_deepCT)

### 3. DeepCT Prediction with MSMARCO and docT5Query Documents

### 4. Generate Dataset File for Converting DeepCT Weights to HDCT Weights

### 5. Combine queries, passage weights to form ANSERINI collection
```
cd $MODEL_HOME
python3 $MODEL_HOME/DeepCT/HDCT/passage2doc_bert_term_sample_to_json_tanh.py $QUERIES $PASSAGE_WEIGHTS $COLLECTION_HDCT 100

```
### 6. Convert the new documents into Anserini JSON format (aka the collection)
```
cd $ANSERINI_HOME
python3 tools/scripts/msmarco/convert_collection_to_jsonl.py \
--collection-path $COLLECTION_HDCT \
--output-folder $COLLECTION_ANSERINI
```

### 7. Generate the Lucene index for the collection of documents
```
sh target/appassembler/bin/IndexCollection -threads 1 -collection JsonCollection \
 -generator DefaultLuceneDocumentGenerator -input $COLLECTION_ANSERINI \
 -index $LUCENE_INDEX -storePositions -storeDocvectors -storeRaw
```

### 8. For dev, perform a simulated leaderboard judgement
```
sh target/appassembler/bin/SearchMsmarco -hits 100 -threads 1 \
 -index $LUCENE_INDEX \
 -queries src/main/resources/topics-and-qrels/topics.msmarco-doc.dev.txt \
 -output $RUN_HOME/runs/run.msmarco-doc.leaderboard-dev.bm25base.txt -k1 0.9 -b 0.4
```

### 9. Evalate the performance
```
python3 tools/scripts/msmarco/msmarco_doc_eval.py \
 --judgments src/main/resources/topics-and-qrels/qrels.msmarco-doc.dev.txt \
 --run $RUN_HOME/runs/run.msmarco-doc.leaderboard-dev.bm25base.txt 
```

# About MSMarco
MS Marco is a collection of research datasets intended to advance AI and related fields.  The document dataset of interest for this work is the MS Marco Document retreval dataset which was released in August of 2020 by Microsoft.  To compare results and create a competative environment which can advance Bing search efficency, Microsoft created the MSMARCO Document Ranking competition and [leaderboard](https://microsoft.github.io/msmarco/).

105 entries have been submitted to the leaderboard.  Many include references to papers, include links the git repository, and include the researchers contributing the submission.  The dataset is divided into train, dev and eval.  Microsoft holds the eval set private and performs the evaluation based on a submitted process.  The MRR (mean reciprical rank 100) evaluation metric is used to judge submission.  This metric takes the average of the inverse position a document returns in a query.  As of 7/19/2021, the leading MRR@100 on Dev is TJ-university using an ensemble model based on ANCE+HDCT+BERT at 0.50.  The Leading eval submission, which is the most important, is a submission from 6/24/2021 by BUPT-University and uses a HNS retrieval and multi-granularity-rerank.  Papers and code are not available for the leading two scores.

Given that the contributions to the MSMARCO Document Ranking Leaderboard do not provide transparent methods, or include peer reviewed papers, the results do not carry as much weight as mainstream academic works.  Regardless, we intend to submit our HDCT+T5 model to the ranking evaluation.


# The MSMARCO data
MS Marco documents contain a document ID, link to the document when it was recorded, the title of the document, and the document text.  Fields in the datafile are tab separated.

```
D301595 http://childparenting.about.com/od/physicalemotionalgrowth/tp/Child-Development-Your-Eight-Year-Old-Child.htm   Developmental Milestones and Your 8-Ye
ar-Old Child    "School-Age Kids Growth & Development Developmental Milestones and Your 8-Year-Old Child8-Year-Olds Are Expanding Their Worlds By Katherine Le
e | Reviewed by Joel Forman, MDUpdated February 10, 2018Share Pin Email Print Eight-year-olds are becoming more confident about themselves and who they are. A
t age 8, your child will likely have developed some interests and hobbies and will know what he or she likes or doesn't like. At the same time, children this
age are learning more about the world at large and are also better able to navigate social relationships with others more independently, with less guidance fr
om parents. At home, 8-year-olds are able to tackle more complicated household chores and take on more responsibility for taking care of themselves, even help
ing out with younger siblings. In general, according to the CDC, these are some changes you may see in your child: Shows more independence from parents and fa
```

The queries assocated with evaluation are delivered in a datafile called msmarco-doctrain-queries.tsv.  Queries are formatted as a query number followed by the full text query valiated by human actors.  The datafile looks like this:

```
1183785 elegxo meaning
645590  what does physical medicine do
186154  feeding rice cereal how many times per day
457407  most dependable affordable cars
441383  lithophile definition
683408  what is a flail chest
484187  put yourself on child support in texas
666321  what happens in a wrist sprain
```

A map is required to match the query to the document that is most closely matched.  This map is used during both training and evaluation to connect a query to a best result.  The mapping file looks like the snippit below:

```
1185855 0 D3202961 1
1185859 0 D2781869 1
1185862 0 D2008201 1
1185864 0 D1126522 1
1185865 0 D630512 1
1185868 0 D59235 1
1185869 0 D59219 1
```

In summary, the distribution of datafiles contains a dev, train, and complete split.  qrels is the map between queries and the docs datafile for the given split.  It is necessary to adhear to the splits for train and dev if you wish to compare results between other runs.
```
-rw-rw-r-- 1 ubuntu ubuntu      108276 May 29 00:27 msmarco-docdev-qrels.tsv
-rw-rw-r-- 1 ubuntu ubuntu      220304 May 29 00:27 msmarco-docdev-queries.tsv
-rw-rw-r-- 1 ubuntu ubuntu    27402095 Jun  1  2019 msmarco-docdev-top100
-rw-rw-r-- 1 ubuntu ubuntu   171213435 Jul  1 16:53 msmarco-docs.pickled-index
-rw-rw-r-- 1 ubuntu ubuntu 22889213781 May 29 01:48 msmarco-docs.tsv
-rw-rw-r-- 1 ubuntu ubuntu     7539008 May 29 01:03 msmarco-doctrain-qrels.tsv
-rw-rw-r-- 1 ubuntu ubuntu    15480364 May 29 01:18 msmarco-doctrain-queries.tsv
-rw-rw-r-- 1 ubuntu ubuntu  1926618965 May 29 01:09 msmarco-doctrain-top100
-rw-rw-r-- 1 ubuntu ubuntu     7139968 Jul 19 22:24 msmarco_docs1000.tsv
-rw-r--r-- 1 root   root        774538 Jun 18 01:45 test.100
```

# Current Results

Model Description | Model Run Number | MRR@100:DEV | Improvement
------------------|------------------|-------------|------------
t5 body only | 1 | 0.267145665 | 0.058250
Baseline msmarco doc | 2 | 0.208895567 | 0.0
tanh passage normalization | 3| 0.248216869 | 0.039321
gaussian passage normalization | 4 | 0.015785233 | -0.19311
t5 body and HDCT body | 5 | 0.266048369 | 0.057153

