# Splitting Documents into Passages

The DeepCT model created by Dai and Callan was initially used on
datasets comprised of text passages that either fit within BERT's
512 token limit, or were truncated to fit within that limit. This is
fine for the MSMARCO passage dataset. But using DeepCT with the
MSMARCO document dataset requires splitting the MSMARCO documents
into passages.

## Document Format for DeepCT
### Output Syntax
DeepCT requries the passages be contained in a text file, with one
passage per line. The syntax is:
```
{passage ID}\t{document text}
```

The passage ID is the MSMARCO document ID with an appended underscore
and passage integer. For example, given a target passage length of 200 words,
MSMARCO document D346879 would be split into 10 passages, with
passage IDs: D346879_0, D346879_1, ..., D346879_9.

### Example Passages
The following excerpt contains two lines of text from one ouput file.

```D1215369_0      Curing Insomnia to Treat Depression Sunday Review | Editorial Curing Insomnia to Treat Depression By THE EDITORIAL BOARD NOV. 23, 2013Psychiatrists have long thought that depression causes insomnia, but new research suggests that insomnia can actually precede and contribute to causing depression. The causal link works in both directions. Two small studies have shown that a small amount of cognitive behavioral therapy to treat insomnia, when added to a standard antidepressant pill to treat depression, can make a huge difference in curing both insomnia and depression in many patients. If the results hold up in other studies already underway at major medical centers, this could be the most dramatic advance in treating depression in decades. A study of 66 patients by a team at Ryerson University in Toronto found that the cognitive therapy for insomnia, a brief and less intense form of talk therapy than many psychiatric patients are accustomed to, worked surprisingly well. Some 87 percent of the patients whose insomnia was resolved in four treatment sessions also had their depression symptoms disappear, almost twice the rate of those whose insomnia was not cured. The new results were reported by Benedict Carey in The Times last Tuesday.
D1215369_1      The brief course of sleep therapy teaches patients to establish a regular wake-up time; get out of bed during waking periods; avoid reading, watching TV or other activities in bed; and eliminate daytime napping, among other tactics. It is distinct from standard sleep advice, like avoiding coffee and strenuous exercise too close to bedtime. The Toronto study is consistent with a 2008 study of 30 patients at Stanford University, all of whom suffered from insomnia and depression and were taking an antidepressant pill. Some 60 percent of those given seven sessions of behavioral therapy for insomnia in addition to the pill recovered fully from their depression, compared with only 33 percent in a control group that got the standard advice for treating sleeplessness. Other studies involving roughly 70 patients each are being conducted at Stanford, Duke University and the University of Pittsburgh, all financed by the National Institute of Mental Health. Those results are expected to be published next year. How these results, if confirmed, will affect clinical practice is uncertain. Most psychiatrists have very little training in dealing with insomnia.
```
## Text Passages from MSMARCO Document Dataset on AWS S3
The full set of passages generated from the MSMARCO document dataset is
available from AWS S3 as a 7.8 GB compressed file at the links below.
An AWS account is required to download the file and download charges may
be incurred. 
* S3 URI: s3://trespi.nir.ucb.2021/msmarco-doc-passages10Jul2021.tar.gz
* URL: https://s3.us-east-2.amazonaws.com/trespi.nir.ucb.2021/msmarco-doc-passages10Jul2021.tar.gz

## Folder Contents

### doc_to_psg.py
`doc_to_psg.py` is a command-line script that takes the msmarco-docs.tsv file
and generates files with one passage per line, suitable for using as an
input to the DeepCT model.

#### Typical Useage
Typical parameters for processing the entire MSMARCO document dataset:
```bash
mkdir passages
python doc_to_psg.py \
    --psg-length 200 \        # Desired number of words in each passage.
    --lines-per-output-file 100000 \ # Number of lines in each output file.
    --num-docs 3213835 \      # Number of lines in input file (for progress bar)
    --output-file passages \  # Output files written to this folder.
    msmarco-docs.tsv
```

Parameters for generating passages from the sample document file:
```bash
mkdir passages
python doc_to_psg.py \
    --psg-length 200 \        # Desired number of words in each passage.
    --lines-per-output-file 1000 \ # Number of lines in each output file.
    --num-docs 1000 \         # Number of lines in input file (for progress bar)
    --output-file passages \  # Output files written to this folder.
    msmarco-docs1000.tsv
```

The `--num-docs` parameter is optional. Including `--num-docs` allows
the progress bar to provide more accurate estimates of remaining time.
The number of documents to process can be obtained by running
`wc -l inputfile.tsv`, for example, `wc -l msmarco-docs.tsv`. 

#### Source Data
The source file must be a TSV file, with the document ID in the first
column, URL in the second column, title in the third, and document text
in the fourth column.

#### Ouput Data
The output files have one passage per line, with a passage ID and the
document contents separated by a tab character. The passage ID has the
syntax: {document id}_{passage number}, with the passage number starting
at zero for the first passage of the document.

`doc_to_psg.py` saves the passages to a sequence of passage files. This
allows prediction with DeepCT to be completed in parallel on multiple
machines.

#### Splitting Technique
`doc_to_psg.py` tries to split documents at sentence boundaries. It uses
nltk's sentence tokenizer to identify sentence boundaries, and adds
sentences to a passage as long as the total word count is less than
the value passed in --psg-length.  Therefore most passages will be
slightly greater than the length specified in --psg-length.

All passages come from a single document. Therefore the final passage of
a document may be shorter than the --psg-length argument.

#### Empty Documents
If both the title and text of a document contain only whitespace, the
document will be skipped.

#### Log
Log messages are written to the file `ouput_log`, including a list of
the files that are skipped due to being empty.

### msmarco-docs1000.tsv
A collection of 1000 documents from the MSMARCO document dataset, provided for
testing of the `doc_to_psg.py` script.
