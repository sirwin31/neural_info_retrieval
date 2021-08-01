# TRESPI
## **TR**ansformers for **E**xpansion of **SP**arse **I**ndexes
This repository contains the code and documentation for TRESPI, our
capstone project for the Masters of Information and Data Science (MIDS)
program at the University of California Berkeley. The project group is
comprised of Joanna Wang, Manpreet Khural, Stacy Irwin, and Wade Holmes.
The project was completed for the Summer 2021 term.

Our research project focuses on this question: Can document indexes for
information retrieval incorporate context AND be supplemented to address
vocabulary mismatch measured by document return rank?

Our project is based on research conducted by Zhuyun Dai and Jamie
Callan at Carnegie Mellon University and Rodrigo Nogueira and Jimmy Lin
at the University of Waterloo.
* [Zhuyun Dai, Jamie Callan. 2020.](https://dl.acm.org/doi/10.1145/3366423.3380258)
Context Aware Term Weighting for Ad-Hoc Search. In
*Proceedings of the Web Conference 2020*, pages 1897-1907.
* [Rodrigo Nogueira, Jimmy Lin.](https://cs.uwaterloo.ca/~jimmylin/publications/Nogueira_Lin_2019_docTTTTTquery-v2.pdf)
*From doc2query to docTTTTTquery.* 2019.

Related Links
* [HDCT Github Repository](https://github.com/AdeDZY/DeepCT)
* [docT5query Github Repository](https://github.com/castorini/docTTTTTquery)

## Description
The HDCT model, described in Dai and Callan's paper, uses a BERT-based
model to generate term-weights for an inverted document index. The
inverted index can be
searched with a probabilistic model like BM25. Instead of basing the
term's weight on its frequency or the number of documents in which it
appears, HDCT evaluates the term's context and estimates the term's
relevance to the document's topic.

The docT5query model uses a T5 sequence-to-sequence model to generate
queries from input text. The queries are related to the input document
in that one would expect the input document to be retrieved in response
to the query being typed into an information retrieval system. 
Nogueira and Lin append the queries to the input document and index the
composite document with BM25 or other probabilistic retrieval models.

While HDCT evaluates the importance of a document term based on its
context, the index developed by HDCT will only match query terms that
appear in the original document, potentially making HDCT indexes
susceptible to vocabulary mismatch. The queries from thedocT5query model
contain relevant terms that do not appear in the input document,
therefore indexed generated by docT5query can potentially address
vocabulary mismatch, however docT5query does not incorporate a term's
context when the index is built.

For our project, we attempted to get the best of both worlds by
combining the HDCT and DocT5query models. We built two document indexes.
Both index were generated from the
[MSMARCO Document dataset](https://microsoft.github.io/msmarco/)
using HDCT. One index was generated using the standard HDCT framework.
The other index was generated from documents comprised solely of queries
generated by docT5query. The two indexes were then combined into a
single index. Our goal is to have an inverted index that reflects a
term's importance within a document, but can also match query terms that
are related to a document's topic but that do not appear in the
document. We named our approach
***TR**ansformers for **E**xpansion of **SP**arse **I**ndexes*,
or TRESPI.

## Repository Structure
Our project code is organized into several subfolders. Each subfolder
contains a README.md file with additional guidance.

Our descripton of the repository structure is in the order that would
be used for processing the dataset and generating a TRESPI document index.

### 1. Generate Dataset from DocT5query
The [docT5query](docT5query) folder contains code related to the
docT5query model. The [docT5query/generate subfolder](docT5query/generate) contains
our PyTorch prediction loop code, which can be used to generate
queries using the
[Huggingface implementation of the docT5query model](https://huggingface.co/castorini/doc2query-t5-base-msmarco). We used an AWS g4dn extra large EC2 instance
to generate queries.

Our single g4dn EC2 instance was not sufficient to generate queries for
all document in the MSMARCO dataset -- we estimated that processing the
entire dataset would take about 1,400 hours. We decided to use queries
that Nogueira and Lin had already generated from the MSMARCO dataset.
See the [docT5query/download subfolder](docT5query/download) subfolder
for guidance on downloading and processing the pre-generated queries.

### 2. DeepCT
The HDCT model uses an earlier model that was developed by Dai and Callan.
The [DeepCT model](https://arxiv.org/abs/1910.10687) uses BERT to generate
passage-level term weights, which are then aggregated into document-level term
weights. In other words, to generate an index using HDCT, one must first
predict terms using DeepCT, then pass the predictions to an HDCT term
aggregation script. Our code related to DeepCT is in the
[deepCT subfolder](deepCT).

There are two steps to using DeepCT. Also, it is necessary to split
documents and run DeepCT predictions twice,
once on the query documents generated by the docT5query model, and
once on the MSMARCO documents.

#### A. Splitting Documents into Passages
The MSMARCO documents must be split into passages. We developed our
own passage splitter for this task, which is in the
[deepCT/doc_split/doc_to_psg.py module](deepCT/doc_split/doc_to_psg.py module).
The `doc_to_psg.py` will write the passages to a sequence of files. The
number of files is determine by the `--docs-per-output-file` argument.
For our project we set `--docs-per-output-file` to 100,000. After
splitting 100,000 documents, the passage-splitting function would begin
writing outtput to a new file. This resulted in the generation of
33 passage files for the MSMARCO Document dataset. The output file are
sequentually numbered, so the document order is maintained.

#### B. Running DeepCT Predictions.
2. Once the passages are split, they can be submitted to the deepCT
prediction step. Running DeepCT predictions requires cloning the
official DeepCT Github repository. Additional guidance is in the
[deepCT/predict/README.md file.](deepCT/predict/README.md)

We ran prediction on AWS g4dn EC2 instances. Generating
predictions on the entire MSMARCO Document dataset required about 60
hours of prediction time. Prediction is easily parallelizable, so we
ran prediction on four EC2 instances in parallel to get elapsed time
down to less than sixteen hours.
* We copied the 33 passage files to all four EC2 instances.
* We ran the
[deepCT/predict/deepct_predict.sh](deepCT/predict/deepct_predict.sh)
script on each instance. The shell script accepts a start and stop file
sequence number, and then runs DeepCT predictions on each passage file
that is within the range of those file sequence numbers.

### 3. HDCT
Additional processing is required before the DeepCT predictions can be
submitted to the HDCT script to generate document-level term weights.
Once that processing is complete, document-level terms are generated by
running a python script. See the README file in the
[HDCT subfolder](HDCT) for details.

### 4. TRESPI
The contents of the TRESPI folder are used to combine the docT5query and
HDCT indexes into a single index. Additional information is available in
the [TRESPI subfolder](TRESPI).

### 5. Generate a Searchable Index
The [Pyserini](https://github.com/castorini/pyserini/) package can be used
to build a searchable index from the document-level term weight files produced
by HDCT. The Pyserini package is a Python wrapper around a Java package named
[Anserini](https://github.com/castorini/anserini), which is a
toolkit for reproducible information retrieval results using
[Lucene](https://lucene.apache.org/). Lucene is an open source Java library
for text indexing and search.

#### A. Installing Anserini and Pyserini
1. Ensure Java 11 is installed. We used OpenJDK. The following command
will install OpenJDK 11 on Ubuntu Linux:
```bash
sudo apt update
sudo apt install openjdk-11-jdk
```
2. Ensure Maven 3.3+, gcc, and make are installed. They can all be installed
with `sudo apt install ___`
3. Set the JAVA_HOME environment variable to the JDK location on your system.
On our Ubuntu machine, we placed the following command in our `.bashrc` file:
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```
4. Follow the instructions in the
[README file for the Anserini repository](https://github.com/castorini/anserini)
to install the Anserini toolkit. This will also install Lucene.
5. Install Pyserini with pip.
```python
pip install pyserini
```
#### B. Convert Term Weights into Anserini JSON format (aka the collection)
```
cd $ANSERINI_HOME
python3 tools/scripts/msmarco/convert_collection_to_jsonl.py \
--collection-path $COLLECTION_HDCT \
--output-folder $COLLECTION_ANSERINI
```
`$COLLECTION_HDCT` is the HDCT term weights file, generated by step 3 or
step 4.

#### C. Generate the Lucene Index
```
sh target/appassembler/bin/IndexCollection -threads 1 -collection JsonCollection \
 -generator DefaultLuceneDocumentGenerator -input $COLLECTION_ANSERINI \
 -index $LUCENE_INDEX -storePositions -storeDocvectors -storeRaw
```
`$COLLECTION_ANSERINI` is the output of the previous step.

### 6. Evaluate Performance
#### A. For dev, perform a simulated leaderboard judgement
```
sh target/appassembler/bin/SearchMsmarco -hits 100 -threads 1 \
 -index $LUCENE_INDEX \
 -queries src/main/resources/topics-and-qrels/topics.msmarco-doc.dev.txt \
 -output $RUN_HOME/runs/run.msmarco-doc.leaderboard-dev.bm25base.txt -k1 0.9 -b 0.4
```

#### B. Evalate the performance
```
python3 tools/scripts/msmarco/msmarco_doc_eval.py \
 --judgments src/main/resources/topics-and-qrels/qrels.msmarco-doc.dev.txt \
 --run $RUN_HOME/runs/run.msmarco-doc.leaderboard-dev.bm25base.txt 
```

## About MSMarco
MS Marco is a collection of research datasets intended to advance AI and related fields.  The document dataset of interest for this work is the MS Marco Document retreval dataset which was released in August of 2020 by Microsoft.  To compare results and create a competative environment which can advance Bing search efficency, Microsoft created the MSMARCO Document Ranking competition and [leaderboard](https://microsoft.github.io/msmarco/).

105 entries have been submitted to the leaderboard.  Many include references to papers, include links the git repository, and include the researchers contributing the submission.  The dataset is divided into train, dev and eval.  Microsoft holds the eval set private and performs the evaluation based on a submitted process.  The MRR (mean reciprical rank 100) evaluation metric is used to judge submission.  This metric takes the average of the inverse position a document returns in a query.  As of 7/19/2021, the leading MRR@100 on Dev is TJ-university using an ensemble model based on ANCE+HDCT+BERT at 0.50.  The Leading eval submission, which is the most important, is a submission from 6/24/2021 by BUPT-University and uses a HNS retrieval and multi-granularity-rerank.  Papers and code are not available for the leading two scores.

Given that the contributions to the MSMARCO Document Ranking Leaderboard do not provide transparent methods, or include peer reviewed papers, the results do not carry as much weight as mainstream academic works.  Regardless, we intend to submit our HDCT+T5 model to the ranking evaluation.


### The MSMARCO data
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

## Current Results

Model Description | RID | tf=avg | tf=pd_avg | Improvement
-----|------|------|-------|------------
Baseline HDCT MSMARCO Doc | - | 0.20889 | 0.22113 | 0.0
t5 body only | 2 | 0.267145665 | nr | 0.05825
tanh passage normalization | 3| 0.24821 | nr | 0.039321
gaussian passage normalization | 4 | 0.01578 | nr|  -0.19311
t5 body and HDCT body | 5 | 0.26604 | nr| 0.057153
Averaging Method | 6 | 0.25065 | nr| 0.04176
Max Method | 7 | 0.26151 | nr| 0.05262
T5 body with tanh | 8 | 0.27155 | 0.278272|  0.06266
T5 body with tanh (optimized k1=10.3, b=0.7) | 8+ | 0.292507| 0.29745 | 0.083617


