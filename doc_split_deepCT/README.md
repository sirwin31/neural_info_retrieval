# Splitting Documents into Passages

The DeepCT model created by Dai and Callan was initially used on
datasets comprised of text passages that either fit within BERT's
512 token limit, or were truncated to fit within that limit. This is
fine for the MSMARCO passage dataset. But using DeepCT with the
MSMARCO document dataset requires splitting the MSMARCO documents
into passages.

## Document Format for DeepCT
DeepCT requries the passages be contained in a text file, with one
passage per line. The syntax is:
```
{passage ID}\t{document text}
```

The passage ID is the MSMARCO document ID with an appended underscore
and passage integer. For example, given a target passage length of 200 words,
MSMARCO document D346879 would be split into 10 passages, with
passage IDs: D346879_0, D346879_1, ..., D346879_9.

## Folder Contents

### doc_to_psg.py
`doc_to_psg.py` is a command-line script that takes the msmarco-docs.tsv file
and generates files with one passage per line, suitable for using as an
input to the DeepCT model.

#### Typical Useage
```bash
mkdir passages
python doc_to_psg.py \
    --psg-length 200 \            # Desired number of words in each passage.
    --lines-per-output-file 200 \ # Number of lines in each output file.
    --num-docs 1000 \             # Number of lines in input file (for progress bar)
    --output-file passages \      # Output files written to this folder.
    msmarco-docs1000.tsv
```

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
