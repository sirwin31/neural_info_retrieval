# DeepCT Model
This folder contains code related to the DeepCT model. While our research
was primarily inspired by Dai and Callan's HDCT model, the HDCT model
includes the DeepCT model.
[The DeepCT model is described in this paper:](https://arxiv.org/abs/1910.10687).
Zhuyun Dai, Jamie Callan. 2019. *Context-Aware Sentence/Passage Term Importance
Estimation For First Stage Retrieval.*

To build the TRESPI index, the following steps must be completed for
both the original MSMARCO documents and for the the queries generated from
the MSMARCO document dataset by docT5query.

## Generating HDCT Prediction Files

### 1. Split Documents into Passages
The [deepCT/doc_split](doc_split) subfolder contains a Python module for
splitting MSMARCO documents into passages that can be fed to the DeepCT
model.

### 1.a Alternative to Step #1: Use Preprocessed Passages Downloaded from AWS S3
A full set of documents and queries that have already been split into
passages for submission to the DeepCT model are available from AWS S3.
The files are formatted as two-column TSV files, with the first column
containing the MSMARCO document ID and passage number, and the second
column containing the document contents. An AWS account is required to
download the files and download charges may be incurred.

### Passages from MSMARCO Document Dataset
The MSMARCO document passages are contained in a 7.8 GB compressed file.
* S3 URI: `s3://trespi.nir.ucb.2021/msmarco-doc-passages10Jul2021.tar.gz`

### Query Passages Generated from DocT5Query
The docT5queries are contained in a 1.6 GB compressed file.
* S3 URI: `s3://trespi.nir.ucb.2021/msmarco_dt5query.tar.gz`

## 2. Predicting Term Importance with DeepCT
The [deepCT/predict](predict) subfolder contains guidance and code for
submitting passages to DeepCT and generating passage-level predictions.

## 2.a Alternative to Step #2: Use Preprocessed Predictions Downloaded from AWS S3

### DeepCT Term Predictions Generated from MSMARCO Documents
The term predictions are contained in a ??? file.
* S3 URI: `s3://trespi.nir.ucb.2021/msmarco_doc_hdct_predictions.tsv.tar.gz`

### DeepCT Term Predictions Generated from DocT5Query Queries
The term predictions are contained in a ??? file.
* S3 URI: `s3://trespi.nir.ucb.2021/doct5query_doc_hdct_predictions.tsv.tar.gz`

## Example Output Data

### 1. Document Passage Files
This section shows example output from step #1, splitting documents
into passages.

#### Example MSMARCO Document Passages
```
D155087_0       What Really Works For Crowâs Feet, Dark Circles, and
Bags What Really Works For Crow’s Feet, Dark Circles, and Bags Facebook
Pinterest Twitter Tumblr0by Wendy Rodewald 22 Shares 3 years ago We all
covet bright, wide-awake eyes, but genes and life’s late nights don’t
always cooperate. That’s why we’re always on the hunt for the best eye
cream to fight dark circles and bags and we’re constantly searching for
the answer on how to get rid of crow’s feet for good. Not sure if your
formula is working? We consulted cosmetic dermatologist Dr. Oscar Hevia,
founder of Hevia MD Skin Science, The Hevia Center for Research and
Hevia Cosmetic Dermatology in Coral Gables, Florida to find out what
really gets the job done right. Dark Circles There are three causes of
dark circles, says Dr. Hevia. “Some people have very thin skin,” he
explains, “so you see the circulation of the blood vessels underneath.”
Others actually have hyperpigmentation under the eyes, which means they
have more melanin concentrated there than in other areas of the face.
D155087_1       A third type is the “shadow effect” which occurs when a
person has a natural hollow under the eye, causing light to reflect in a
way that creates a dusky look there. Many people have two or three of
these issues at the same time. What you can do: Since only one of the
three causes of dark circles is on the skin’s surface, topical creams
are really only effective for hyperpigmentation, Dr. Hevia explains.
Look for products that include Vitamin C, the lightening agent
hydroquinone, and non-hydroquinone lightening ingredients such as kojic
acid and arbutin. Murad Lighten and Brighten Eye Treatment ($67,
dermstore.com) contains 1.5% hydroquinone that’s safe to use under the
eyes. Vichy Pro EVEN Daily Eye Corrector ($39.50, vichyusa.com) targets
dark circles and spots with Ceramide Bright, a non-hydroquinone
ingredient that regulates melanin and also moisturizes. When the derm
can do: If you have one of the other two types — circulatory or shadows
— hyaluronic acid gel fillers, such as Juvéderm, are your best bet.
```

#### Example DocT5Query Passages
```
D947688_0       U.S. Anti-Trafficking Legislation what is the purpose of
trafficking victim protection act? what is trafficking victims
protection act definition? what is the tvpa in 5 colors? what the tvpa
in 5 colors? who is protected under the tvpa? what does the tvpa protect
against? what is the purpose of the tvpa? what does the trafficking
victim protection act (tvpa) do? what is tvpa law? when was the
Trafficking Victims Protection Act of 2000 enacted? D288607_0
Peterborough where is peterborough? where is peterborough uk? where is
peterborough? where is peterborough? where is peterborough? where is
peterborough uk? where is peterborough? what region is peteborough? what
is the population of peterborough? where is peterborough located? which
region is peterborough, uk in? when did peterborough become a town? what
is peterborough known for? what is the history of peterborough? why is
peteborough england a city? what was the population of peterborough? who
settled peterborough? what was the town of peterborough's first name?
where is peterborough? where is peterborough? what is the peterborough?
when was peterborough peterborough built? where does the town of
peterborough live? why is peterborough in the english? history of
peterborough borough? what year is peteborough uk founded? what was
peterborough originally known as? why is the town of peterborough a city
centre? where was peterborough? what is the population of peterborough
uk? when did peterborough become a city? what was the roman settlement
of peterborough? where was peterborough roman settlement at? D288607_1
when was peterborough established? where was peterborough, england
originally? where is peterborough? where was peterborough founded? which
roman town was named after the fort of langthorpe? when was peterborough
established? when was peterborough england? where is tout hill located?
where is the abbey of peterborough? when did peterborough become a
scottish village? who founded peterborough? why was peterborough called
tout hill? where was the peterborough abbey located and why? where is
the turold castle? when was peterborough established by edwin turold?
where was peterborough? where is peterborough? who settled in
peterborough? when was peterborough cathedral built? when did the city
of peterborough become a cathedral? when was peterborough founded? when
did peterborough get its name? when did peterborough cathedral open?
where is peterborough cathedral in england? what is the peterborough
cathedral? what was the king's first charter for peterborough? when was
peterborough england founded? when did the abbott build peterborough
cathedral? when was borough of peterborough incorporated? what city is
known for its cathedral? what was the borough that fought civil war?
```
### 2. Example Prediction Files
The prediction files contain terms and unscaled term weights. Each line
contains terms for a single passage. Note that the prediction file
does not list the document IDs for each document. HDCT assumes that the
document order in the prediction file is the same as the document order
in in the passage file (see step 1).
```
developmental 0.13003   milestone 0.09904       ##s 0.00000     and
0.00176     your 0.00262    8 0.69739       - 0.00359       year 0.01532
- 0.00198       old 0.77808     child 0.34003   " -0.00157      school
0.19971  - 0.00029      age 0.76589      kids 0.12798    growth 0.04097
& 0.00045       development 0.09671     developmental 0.12033
milestone 0.10713       ##s 0.00000     and 0.00153     your 0.00220
8 0.70346       - 0.00214       year 0.00657    - 0.00143       old
0.76672     child 0.00385   ##8 0.00000     - 0.00111       year 0.00310
- 0.00133       olds 0.52602   are -0.00031     expanding 0.00349
their -0.00141  worlds 0.00261  by -0.00120     katherine 0.00158
lee 0.00402     | 0.00003       reviewed 0.00167        by 0.00005
joel 0.00189    form 0.00922    ##an 0.00000    , -0.00015      md
0.00152      ##up 0.00000    ##date 0.00000  ##d 0.00000     february
-0.00006       10 -0.00008     , -0.00069      2018 0.00063    ##sha
0.00000   ##re 0.00000    pin 0.00225     email 0.00101   print 0.00281
eight 0.59518  - 0.00249        year 0.00725    - 0.00127       olds
0.56249    are -0.00024    becoming 0.00243        more -0.00015
confident 0.00892        about -0.00050  themselves 0.00084      and
-0.00041    who 0.00222     they -0.00122   are -0.00033    . 0.00057
at -0.00056     age 0.77786     8 0.56693       , -0.00071      your
-0.00009   child 0.31707  will -0.00068    likely 0.00085  have -0.00081
developed 0.04078       some -0.00060   interests 0.00566       and
-0.00079    ho 0.00442      ##bbies 0.00000 and -0.00039    will
-0.00017   know 0.00045    what -0.00065   he -0.00022    or -0.00054
she 0.00050     likes 0.00203   or -0.00105     doesn 0.00040   '
-0.00030      t 0.00008       like 0.00030    . -0.00025      at
-0.00100     the -0.00141    same -0.00040   time 0.00287    , -0.00097
children 0.1750this -0.00188    age 0.75914     are -0.00024    learning
0.01321        more -0.00159   about -0.00135  the -0.00260   world
0.01216    at -0.00157     large -0.00073  and -0.00134    are -0.00108
also -0.00081   [SEP] -0.00000
parents 0.07578 and 0.00112     other
0.00303   significant 0.01109     adults 0.10908  in -0.00062     the
0.00050    child 0.45760    ' -0.00009      s 0.00065       life 0.02715
should -0.00022 keep 0.00934    in -0.00243     mind 0.00604    the
-0.00031    importance 0.06924      of -0.00210     being 0.00038   good
0.09364    role 0.07159    models 0.03813  since -0.00125  this -0.00073
is -0.00154     a -0.00126      time 0.01731    when -0.00162   children
0.2561are -0.00002     figuring 0.00453        out -0.00086    the
-0.00109    world 0.00455   and 0.00041     who 0.00283    they -0.00054
are -0.00009    and 0.00074     how 0.00098     they -0.00075   fit
0.00460     into 0.00138    it -0.00179     . 0.00114       at -0.00040
this -0.00058   age 0.49811     , 0.00101       your -0.00050   child
0.43943  may -0.00083     get 0.00178     involved 0.01256        with
-0.00041   more 0.00087    complex 0.00928 social 0.05403 activities
0.02517       and -0.00012    behaviors 0.06635       that 0.00007
help 0.07036    define 0.01420  his 0.00189     or 0.00147      her
0.00173     sense 0.00784   of -0.00043     self 0.03782    . 0.00155
effective 0.03833       discipline 0.85369      techniques 0.06095
at -0.00077     this -0.00079   age 0.43726     include
0.00119continuing 0.00325       to -0.00032     praise 0.00807  good
0.07559    behavior 0.06260        , 0.00056       focusing 0.00445
your 0.00019    child 0.40521   ' -0.00030      s -0.00032      efforts
0.00280 , 0.00045       what 0.00042    they -0.00047   can -0.00011
do 0.00208      and -0.00034    change 0.00495  , 0.00002       rather
-0.00035than -0.00037    innate 0.00837  traits 0.01270  ( -0.00005
such 0.00107    as 0.00025      " -0.00038      " -0.00054      you
-0.00130    are -0.00117    smart 0.01640   " -0.00021      " -0.00037
) -0.00023      . 0.00004      set 0.00840      up -0.00113     and
0.00007     enforce 0.00631 consistent 0.00480      rules 0.01018   .
0.00145      discipline 0.87108       should 0.00260  be 0.00008
aimed 0.00737   at 0.00269      [SEP] -0.00000
```