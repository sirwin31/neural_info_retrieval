# DocT5Query Model
This folder contains code related to the docT5query model.

## Query Generation from docT5query
The [generate subfolder](generate) contains
our PyTorch prediction loop code, which can be used to generate
queries.

## Use Queries Pre-generated Queries
Noguiera and Lin have already generated queries for the MSMARCO Document
dataset and made those queries available online. The
[download subfolder](download) contains a script that will convert
the downloaded queries into a format suitable for submission to the HDCT
model.

Nogueira and Lin split the documents from the MSMARCO documenent dataset into
passages and generated ten queries per passage. A single document may have
ten to several hundred queries, depending on its length.

## Use Preprocessed Passages Downloaded from AWS S3
A full set of queries that have already been converted into a format similar
to the MSMARCO document dataset is available from AWS S3 as a 1.6 GB compressed file.
An AWS account is required to download the file and download charges may
be incurred. The S3 URI is `s3://trespi.nir.ucb.2021/msmarco_dt5query.tar.gz`.

The file can be downloaded using AWS CLI. For example:
```bash
aws s3 cp s3://trespi.nir.ucb.2021/msmarco_dt5query.tar.gz msmarco_dt5query.tar.gz
```

The file is formatted as a TSV file with four columns: MSMARCO document ID, 
URL, title, and text.

The compressed file expands to a set of 33 files that are formatted for submission
to the DeepCT model. Each file is a TSV
file with two columns. The first column contains the MSMARCO document ID
and passage number, and the second column contains the queries. For example:
```
D1659457        http://www.ushistory.org/us/11.asp      11. The American
Revolution what did the minutemen fight? what were the minutes during
the american revolution? what was the american revolution? where were
minutemen? what was the american revolution? what was one obstacle to
the battle of lexington and concord? what was the american revolution?
why were minute men called minutemen? why americans were the minutemen
of the revolutionary war? what year did the american revolution start?
when was bunker hill fought? how did the american revolutionary war
happen? who did the colonists defeat? when were the battles of bunker
hill? why did the american revolution take place? ...
```