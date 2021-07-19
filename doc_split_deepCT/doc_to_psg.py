"""Splits documents into passages suitable for processing by DeepCT.

Creating term indexes with HDCT or DeepCT from copora of longer
documents (documents that exceed BERT's 512 token limit) requires
splitting the documents into shorter passages. the `doc_to_psg.py`
module will convert MSMARCO documents to shorter passages that can
be passed to a BERT-based model like DeepCT.

This module is intended to be run from the command line. It was
constructed specifically to split documents from the MSMARCO *document*
dataset.

Typical useage:
```bash
mkdir passages
python doc_to_psg.py \
    --psg-length 200 \  # Desired number of words in each passage.
    --lines-per-output-file 200 \ # Number of lines in each output file.
    --num-docs 1000 \ # Number of lines in input file (for progress bar)
    --output-file passages \  # Output files written to this folder.
    msmarco-docs1000.tsv
```

Other available arguments:
    --num-docs NNN: positive integer, used for testing. Only processed
                    the first NNN documents.

Source Data:
The source file must be a TSV file, with the document ID in the first
column, URL in the second column, title in the third, and document text
in the fourth column.

Ouput Data:
The output files have one passage per line, with a passage ID and the
document contents separated by a tab character. The passage ID has the
syntax: {document id}_{passage number}, with the passage number starting
at zero for the first passage of the document.

Splitting Technique:
doc_to_psg tries to split documents at sentence boundaries. It uses
nltk's sentence tokenizer to identify sentence boundaries, and adds
sentences to a passage as long as the total word count is less than
the value passed in --psg-length.

Empty Documents:
If both the title and text of a document contain only whitespace, the
document will be skipped.

Log:
Log messages are written to the file `ouput_log`, including a list of
the files that are skipped due to being empty.
```
"""

import argparse

import nltk 
import nltk.tokenize
from tqdm import tqdm


# Command line arguments
desc = """Converts msmarco-docs.tsv data to passages file that can
be used for DeepCT predictions."""
parser = argparse.ArgumentParser(desc)
parser.add_argument('--output-file', help='Path to output file')
parser.add_argument('--psg-length', type=int, default=275,
                    help='Target passage length')
num_docs_help = 'Expected number of docs in input file'
parser.add_argument('--num-docs', type=int, default=None,
                    help=num_docs_help)
parser.add_argument('--lines-per-output-file', type=int, default=100_000,
                    help='Number of lines in each output file.')
parser.add_argument('path', help='Path to TSV file with MS Marco documents')


def split(doc_path, output_path, psg_len, output_num_lines, doc_total=None):
    """Splits a MSMARCO TSV file into separate passages.

    Args:
        doc_path: str, full path to MSMARCO document file.
        output_path: The name of the folder where the output documents
            will be written.
        psg_len: The target length of each passage.
        output_num_lines: The length of each output file, in lines.
        doc_total: Number of documents in input file. Optional. Used
        so progress bar will provide an accurate estimate of time
        remaining. Get number of lines with `wc -l input_file`.
    """
    with open(doc_path, 'rt') as dfile, open('log_file', 'wt') as lfile:
        output_file_num = 0
        ofile = None
        for idx, line in tqdm(enumerate(dfile), 'Docs Processed', doc_total):
            # Start writing output to a new file
            if idx % output_num_lines == 0:
                full_output_path = ('{}_{:03d}.tsv'
                                    .format(output_path, output_file_num))
                if ofile is not None:
                    ofile.close()
                ofile = open(full_output_path, 'wt')
                print('Writing to file:', full_output_path)
                output_file_num += 1
            doc_id, url, title, text = line.split('\t')
            text = text[:-1] if text[-1] == '\n' else text

            # Verify that document is not empty
            check_text = title+text
            if check_text.isspace() or not check_text:
                msg = 'Skipping doc {} due to no data!'.format(doc_id)
                print(msg)
                lfile.write(msg + '\n')
                continue

            # Assemble Passages
            sentences = nltk.tokenize.sent_tokenize(title + ' ' + text)
            sent_lengths = [len(nltk.tokenize.word_tokenize(sentence))
                            for sentence in sentences]

            passage = []
            psg_num = 0
            start_idx = 0
            for idx, sentence in enumerate(sentences):
                end_idx = start_idx + len(passage)
                curr_len = sum(sent_lengths[start_idx:end_idx])
                if curr_len < psg_len:
                    passage.append(sentence)
                else:
                    ofile.write("{}_{}\t{}\n".format(doc_id, psg_num, ' '.join(passage)))
                    passage = []
                    passage.append(sentence)
                    start_idx = idx
                    psg_num += 1
            ofile.write("{}_{}\t{}\n".format(doc_id, psg_num, ' '.join(passage)))
    ofile.close()
    lfile.close()


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    split(args.path,
          args.output_file,
          args.psg_length,
          args.lines_per_output_file,
          args.num_docs)
