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

## 1. Split Documents into Passages
The [deepCT/doc_split](doc_split) subfolder contains a Python module for
splitting MSMARCO documents into passages that can be fed to the DeepCT
model.

## 2. Predicting Term Importance with DeepCT
The [deepCT/predict](predict) subfolder contains guidance and code for
submitting passages to DeepCT and generating passage-level predictions.

## Use Preprocessed Passages Downloaded from AWS S3
A full set of documents and queries that have already been split into
passages for submission to the DeepCT model are available from AWS S3.
The files are formatted as two-column TSV files, with the first column
containing the MSMARCO document ID and passage number, and the second
column containing the document contents. An AWS account is required to
download the files and download charges may be incurred.

### MSMARCO Document Passages
The MSMARCO document passages are contained in a 7.8 GB file.
* S3 URI: `s3://trespi.nir.ucb.2021/msmarco-doc-passages10Jul2021.tar.gz`

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

### Queries Generated from DocT5Query
The docT5queries are contained in a 1.6 GB file.
* S3 URI: `s3://trespi.nir.ucb.2021/msmarco_dt5query.tar.gz`

#### Example Query Passages
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
