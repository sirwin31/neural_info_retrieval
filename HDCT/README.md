# Generating Document-Level Term Weights with HDCT
The DeepCT repository contains a
[python script for generating HDCT term weights from passage-level weights](https://github.com/AdeDZY/DeepCT/tree/master/HDCT). The script requires two input
documents.

## Input Files
1. The first input document is a predictions file, containing passage-level
term weights. See the README.md file in the [deepCT subfolder](deepCT) for
more detail on prediction files.
2. The second input document is a JSONL document, where each line is a
dictionary with keys 'id', 'url', and 'title'. The value of the 'id' key
is the document ID and passage number, connected with an underscore. For
example, the 'id' value for the 2nd passage of document ID D178296 would be
`D178296_1`. Since the predictions file does not contain document IDs, the HDCT
python script uses the JSONL dataset file to align passages with their
documents.

## Generating Document-Level Weights
### Original HDCT Script
If the dataset filename is `dataset.jsonl`, the predictions file is
`predictions.tsv`, and the output is to be written to `hdct_weights.json`, the
command to generate the HDCT term weights from the DeepCT passage-level
predictions is:

```bash
python3 ~/DeepCT/HDCT/passage2doc_bert_term_sample_to_json.py \
    --tf_agg_method position_decay_avg \
    dataset.jsonl \
    predictions.tsv \
    hdct_weights.json \
    100
```

The final parameter, 100, is the scaling factor that the passage-level
weights will be multipled by. Dai and Callan recommend using 100.

### Parameters for `passage2doc_bert_term_sample_to_json.py`
* **dataset_file:** JSONL file that matches predictions to document IDs and
    passages.
* **prediction_file:** TSV file that contains DeepCT passage-level weights.
* **output_file:** Document-level term weights will be written to this file.
* **m:** Passage-level weights will be scaled by taking the square root and
    multiplying by this factor.
* **--output_format:** tsv or json
* **--tf_agg_method:** avg, sum, position_decay_avg, or position. See 
Dai and Callan's paper on DeepCT for additional information. The best
performance is expected with position_decay_avg.
* **--max_number_passages:** Specifies the maximum number of passages
that will be processed.

### Modified TRESPI Hyperbolic Tangent Script
For TRESPI, we replaced the square root function that is used when scaling
term weights with a hyperbolic tanget function. To use the hyperbolic tangent
function, use the `HDCT/passage2doc_bert_term_sample_to_json_tanh.py` script.
The parameters and syntax are identical to those for the
`passage2doc_bert_term_sample_to_json.py` script.

## Download Document-Level Termweights from AWS
Document-level HDCT-generated term weights are available for download from
AWS S3.
* **MSMARCO Document HDCT Termweights:**: `s3://trespi.nir.ucb.2021/msmarco_hdct_docweights.tar.gz`
* **DocT5Query HDCT Termweights:**: `s3://trespi.nir.ucb.2021/doct5query_hdct_docweights.tar.gz`

## Example Document-Level Weights
Both HDCT scripts discussed in this document generate a JSONL file, with each
line containing the term weights for a single document. Each line consists of
a dictionary with two keys: 'id' and 'contents'. The 'id' value is the
document ID, and the 'contents' value containts all index terms. The terms
are repeated according to their term weight. For example, in the example
document below, the term "developmental" has a term weight of 25, so it is
repeated 25 times.

A single document is shown 
```
{"id": "D301595", "contents": "developmental developmental developmental
developmental developmental developmental developmental developmental
developmental developmental developmental developmental developmental
developmental developmental developmental developmental developmental
developmental developmental developmental developmental developmental
developmental milestones milestones milestones milestones milestones
milestones milestones milestones milestones milestones milestones
milestones milestones milestones milestones milestones milestones
milestones and and your your 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 year year
year year old old old old old old old old old old old old old old old
old old old old old old old old old old old old child child child child
child child child child child child child child child child child child
child child child child child child child child child child child child
child child child child child child child child child child child child
child child child child child child child child child child child school
school school school school school school age age age age age age age
age age age age age age age age age age age age age age age age age age
age age age age age age age age age age age age age age age age age age
age kids kids kids kids kids kids kids kids kids kids kids kids kids
kids kids growth growth growth development development development
development development development development development development
development development development development development development
development development development development development development
development development development development development child8 olds
olds olds olds olds olds olds olds olds olds olds olds expanding lee
forman eight eight eight eight eight eight eight eight eight eight eight
eight eight eight confident who developed developed developed interests
interests interests hobbies time time time time time time time time time
time time time children children children children children children
children children children children children children children children
children children children children children children children children
children children children children children children children children
children children children children children children children children
children children children children children learning world world world
world parents parents parents parents parents parents other significant
adults adults adults adults adults the s s life life keep mind
importance importance importance importance good good good good good
good good good good good good good good good good role role role role
models models models figuring fit involved more complex social social
social activities activities behaviors behaviors behaviors behaviors
help help help help help help help help help help help help help define
define his her sense sense sense self self self self self self self self
self self self effective effective effective discipline discipline
discipline discipline discipline discipline discipline discipline
discipline discipline discipline discipline discipline discipline
discipline techniques techniques techniques techniques continuing praise
behavior behavior behavior behavior focusing what change innate traits
smart smart set enforce consistent rules be aimed at at at this needs
needs hours hours hours hours sleep sleep sleep sleep sleep sleep sleep
night night physical physical physical physical physical physical
physical physical image getty getty getty images images images for
refinement skills skills skills skills coordination muscle control
changes changes begin look look big big big big \" \" \" puberty puberty
puberty puberty puberty puberty years years years years away away away
away natural natural athletic athletic athletic athletic potential
potential show abilities stage stage stage stage stage stage stage
precise accurate decide decide is developing developing developing
developing developing developing developing developing developing
developing developing developing developing developing sophisticated
himself talents friends relationship family establish clear identity
beginning beginning desiring desiring privacy flip confidence confidence
doubt develop develop develop develop develop develop develop develop
develop develop develop develop develop develop patience empathy empathy
others others cognitive cognitive cognitive cognitive cognitive tom
merton intellectual intellectual intellectual intellectual intellectual
able pay attention longer periods expect expect discuss discuss
respecting different different different different different different
provide professionals tool comparing comparing norm norm norm fits fits
ideal ideal ideal perfectly personal quirks strengths challenges
preferences said feel ahead worth discussing discussing discussing issue
issue pediatrician pediatrician pediatrician pediatrician teacher
teacher teacher issues opportunities learn learn learn about address
word middle middle middle middle middle middle middle middle middle
middle middle middle middle middle middle middle childhood childhood
childhood childhood childhood childhood childhood childhood childhood
childhood childhood childhood childhood childhood childhood cdc cdc cdc
cdc"}
```