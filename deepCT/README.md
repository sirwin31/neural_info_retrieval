## Use Preprocessed Passages Downloaded from AWS S3
A full set of queries that have already been processed for submission to
the DeepCT model is available from AWS S3 as a 1.6 GB compressed file.
An AWS account is required to download the file and download charges may
be incurred. The S3 URI is `s3://trespi.nir.ucb.2021/msmarco-doc-passages10Jul2021.tar.gz`.

The file can be downloaded using AWS CLI. For example:
```bash
aws s3 cp s3://trespi.nir.ucb.2021/dt5_msmarco_query_passages.tar.gz dt5_msmarco_query_passages.tar.gz
```

The compressed file expands to a set of 33 files that are formatted for submission
to the DeepCT model. Each file is a TSV
file with two columns. The first column contains the MSMARCO document ID
and passage number, and the second column contains the queries. For example:
```
D947688_0       U.S. Anti-Trafficking Legislation what is the purpose of trafficking victim protection act? what is trafficking victims protection act definition? what is the tvpa in 5 colors? what the tvpa in 5 colors? who is protected under the tvpa? what does the tvpa protect against? what is the purpose of the tvpa? what does the trafficking victim protection act (tvpa) do? what is tvpa law? when was the Trafficking Victims Protection Act of 2000 enacted?
D288607_0       Peterborough where is peterborough? where is peterborough uk? where is peterborough? where is peterborough? where is peterborough? where is peterborough uk? where is peterborough? what region is peteborough? what is the population of peterborough? where is peterborough located? which region is peterborough, uk in? when did peterborough become a town? what is peterborough known for? what is the history of peterborough? why is peteborough england a city? what was the population of peterborough? who settled peterborough? what was the town of peterborough's first name? where is peterborough? where is peterborough? what is the peterborough? when was peterborough peterborough built? where does the town of peterborough live? why is peterborough in the english? history of peterborough borough? what year is peteborough uk founded? what was peterborough originally known as? why is the town of peterborough a city centre? where was peterborough? what is the population of peterborough uk? when did peterborough become a city? what was the roman settlement of peterborough? where was peterborough roman settlement at?
D288607_1       when was peterborough established? where was peterborough, england originally? where is peterborough? where was peterborough founded? which roman town was named after the fort of langthorpe? when was peterborough established? when was peterborough england? where is tout hill located? where is the abbey of peterborough? when did peterborough become a scottish village? who founded peterborough? why was peterborough called tout hill? where was the peterborough abbey located and why? where is the turold castle? when was peterborough established by edwin turold? where was peterborough? where is peterborough? who settled in peterborough? when was peterborough cathedral built? when did the city of peterborough become a cathedral? when was peterborough founded? when did peterborough get its name? when did peterborough cathedral open? where is peterborough cathedral in england? what is the peterborough cathedral? what was the king's first charter for peterborough? when was peterborough england founded? when did the abbott build peterborough cathedral? when was borough of peterborough incorporated? what city is known for its cathedral? what was the borough that fought civil war?
```