"""Functions for generating queries with doc2query-T5
"""
import os.path
import sys

import nltk.tokenize
import torch
import torch.utils.data
import transformers

dirname = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(dirname, '../..'))
sys.path.insert(0, repo_root)
import util.indexer

MODEL_NAME = 'castorini/doc2query-t5-base-msmarco'
BASE_MODEL_NAME = 't5-base'


# Dataset should return docid, pos, passage


class DocDataset(torch.utils.data.IterableDataset):
    """Pytorch dataset -- can be fed to Pytorch models.
    """
    def __init__(self,
                 doc_path,
                 doc_batch_size=1000,
                 max_len=512,
                 tgt_len=256,
                 min_len=128,
                 max_passages=None,
                 max_docs_in=None,
                 fast_tokenizer=True):
        """Initializes dataset object.
                Args:
                    doc_path: String, path to msmarco tsv file with
                            documents
                    max_len: int, the maximum allowed sequence length.
                            Sentences will be split if needed to stay
                            below this limit.
                    tgt_len: int, target sequence length. `split_doc`
                            will not add additional sentences once this
                            length is achieved.
                    min_len: int, minimum allowed sequence length.
                            Sentences will be split if needed to stay
                            above this limit.
                    max_passages: int, dataset will stop sending data
                            after the number of specified passages are
                            generated. Default of None means all data in
                            file will be processed.
                    max_docs: int, dataset will stop sending data
                            after the number of specified documents
                            are generated. Default of None means all
                            data in file will be processed.
        """
        super(DocDataset).__init__()
        self.doc_path = doc_path
        self.doc_idx = util.indexer.IndexedFile(doc_path, 0, line_idx=True)
        self.max_len = max_len
        self.tgt_len = tgt_len
        self.min_len = min_len
        self.fast_tokenizer = fast_tokenizer
        if self.fast_tokenizer:
            self.tokenizer = transformers.T5TokenizerFast.from_pretrained(
            BASE_MODEL_NAME)
        else:
            self.tokenizer_model = transformers.T5Tokenizer.from_pretrained(
                MODEL_NAME)
        self.max_passages = max_passages
        self.passage_generator = None
        self.max_docs = max_docs_in
        self.doc_batch_size = 1000 if doc_batch_size is None else doc_batch_size

    def init_passage_generator(self):
        num_passages = 0
        doc_counter = 0
        num_lines = len(self.doc_idx)
        line_pos = min(self.doc_batch_size, num_lines-1)
        start_byte_pos = 0
        self.dfile = open(self.doc_path, 'rb')
        while line_pos < num_lines:
            print(f'Reading next {line_pos + 1} documents')
            end_byte_pos = self.doc_idx.lines[line_pos][0]
            if line_pos < num_lines-1:
                data = self.dfile.read(end_byte_pos - start_byte_pos)
                line_pos = min(line_pos + self.doc_batch_size, num_lines-1)
            else:
                data = self.dfile.read()
                line_pos = num_lines
            start_byte_pos = end_byte_pos
            text =  data.decode('utf-8')
            lines = text.split('\n')

            for line in lines:
                if line == '':
                    return
                if self.max_docs is not None and doc_counter >= self.max_docs:
                    return
                doc_counter += 1
                split_line = line.split('\t')
                doc = {'docid': split_line[0],
                        'url': split_line[1],
                        'title': split_line[2],
                        'text': split_line[3]}
                passages = self.split_doc_text(doc['title'] + ' ' + doc['text'])
                for passage in passages:
                    if (self.max_passages is not None and
                            num_passages >= self.max_passages):
                        return
                    num_passages += 1
                    yield (doc['docid'], passage['position'],
                            torch.tensor(passage['input_ids']),
                            torch.tensor(passage['attention_mask']))


    def __iter__(self):
        self.passage_generator = self.init_passage_generator()
        return self

    def __next__(self):
        return next(self.passage_generator)

    def close(self):
        self.dfile.close()

    def split_doc_text(self, doc_text):
        """Splits document at sentence boundaries and tokenizes for T5.
        
        Args:
            doc: String, the document to be split
                
        Returns:
            A list of dictionaries, with one dictionary per passage.
            The keys are:
                pos: passage position within document, starting at 0.
                input_ids: token ID values generated by T5 tokenizer
                attention_mask: List of ones that are the same length as
                    the input_ids.
        """
        # Create list of (sentence position, sentence length, list of T5 input
        #     IDs, passage_id)
        tokenized_sentences = [self.tokenizer(sentence)['input_ids']
                            for sentence
                            in nltk.tokenize.sent_tokenize(doc_text)]
        sentence_data = [(pos, len(sentence), sentence)
                    for pos, sentence in enumerate(tokenized_sentences)]
        
        passage = []    
        passages = []
        for sentence in sentence_data:
            curr_len = len(passage) + sentence[1]
            if curr_len <= self.tgt_len:    # Too short - add another sentence
                passage.extend(sentence[2]) 
            elif curr_len <= self.max_len:  # Just right, start another passage
                passage.extend(sentence[2])
                passages.append(passage)   
                passage = []
            else:                           # Oh-oh, above max length
                if len(passage) > self.min_len:  # Reached min length
                    passages.append(passage)     #   Start next passage
                    passage = sentence[2]
                else:            # Did not reach min len, break up sentence.
                    sentence_break = self.max_len - len(passage)
                    passage.extend(sentence[2][:sentence_break])
                    passages.append(passage)
                    passage = sentence[2][sentence_break:]
                while len(passage) > self.max_len:  # Longer than max_len
                    passages.append(passage[:self.max_len])
                    passage = passage[self.max_len:]
        if len(passage) > 0:  # Don't forget to append final passage.
            passages.append(passage)

        # Pad all passages and masks to self.max_len
        padded_passages = []
        for pos, passage in enumerate(passages):
            passage_len = len(passage)
            padding_len = self.max_len - passage_len
            padding = [0] * padding_len
            passage.extend(padding)
            attention_mask = [1] * passage_len
            attention_mask.extend(padding)
            padded_record = {'position': pos,
                             'input_ids': passage,
                             'attention_mask': attention_mask}
            padded_passages.append(padded_record)

        return padded_passages
