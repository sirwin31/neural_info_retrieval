import argparse
import itertools
import sys

import torch
from torch._C import clear_autocast_cache
import torch.utils.data
import transformers

sys.path.append('/home/ubuntu/neural_info_retrieval/TRESPI')
import batched_dataset as ds
import util.log

MODEL_NAME = 'castorini/doc2query-t5-base-msmarco'

# Set up command-line arguments.
desc = ('Uses the doc2query-T5 model to generate queries from '
        'source documents.')
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('path', help='Path to TSV file with MS Marco documents')
parser.add_argument('--output-file', help='Path to output file')
parser.add_argument("--psg-max", type=int, default=128,
                    help='Maximum allowed length of source document passages')
parser.add_argument("--psg-min", type=int, default=32,
                    help='Minimum allowed length of source document passages')
parser.add_argument("--psg-tgt", type=int, default=64,
                    help='Target length of source document passages')
parser.add_argument('--num-queries', type=int, default=3,
                    help='The number of queries to generate for each passage')
parser.add_argument('--max-psg-in', type=int,
                    help='Stop after generating queries for this many passages.'
                         ' Default is to use all passages in docs file')
parser.add_argument('--qry-len', type=int, default=64,
                    help='Max length of generated queries')
parser.add_argument('--t5-batch-size', type=int, default=16,
                    help='Batch size for inputs to doc2query-T5')
parser.add_argument('--max-docs-in', type=int,
                    help='Stop after generating queries for this many documents.'
                         ' Default is to use all documents file')
parser.add_argument('--doc-read-batch-size', type=int,
                    help='Number of documents to read from disk at one time')

def expand_list(data, reps):
    """Creates longer list by repeating elements in list.

    Example: expand_list([1, 2, 3], 3) returns
    [1, 1, 1, 2, 2, 2, 3, 3, 3]
    """
    nested_list = [[datum] * reps for datum in data]
    flat_list = list(itertools.chain(*nested_list))
    return flat_list


def generate_queries():
    args = parser.parse_args()

    # Setup logging and display startup messages
    logger = util.log.get('Query_generation_doc2queryT5')
    logger.info('Starting Query Generation with doc2qury-T5')
    for arg, val in vars(args).items():
        logger.info(f'Argument - {arg:>14}: {val}')


    # Prepare the source documents
    doc_dataset = ds.DocDataset(args.path,
                                doc_batch_size=args.doc_read_batch_size,
                                min_len=args.psg_min,
                                tgt_len=args.psg_tgt,
                                max_len=args.psg_max,
                                max_passages=args.max_psg_in,
                                max_docs_in=args.max_docs_in)
    logger.info('Created document dataset')
    doc_loader = torch.utils.data.DataLoader(
        doc_dataset,
        batch_size=args.t5_batch_size
    )
    logger.info('Created document loader')

    # Tokenizer will convert model output back to text
    tokenizer = transformers.T5Tokenizer.from_pretrained(MODEL_NAME)
    logger.info(f'Initialized tokenizer for {MODEL_NAME}')

    # Create model and send to GPU
    device_name = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = torch.device(device_name)
    logger.info(f'Initializing model and sending to {device_name}')
    model = transformers.T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    model.to(device)
    model.eval()
    logger.info('Model initialized')

    # Query Generation Loop
    ofile = open(args.output_file, 'wt')
    for batch_num, batch in enumerate(doc_loader):
        logger.info(f'Starting batch {batch_num + 1}')
        # Setup model inputs
        doc_ids = expand_list(batch[0], args.num_queries)
        positions = expand_list(batch[1], args.num_queries)
        input_ids = batch[2].to(device)  # To GPU
        mask = batch[3].to(device)       # To GPU

        # Run a batch through T5 model
        with torch.no_grad():
            outputs = model.generate(
                input_ids = input_ids,
                attention_mask = mask,
                max_length=args.qry_len,
                do_sample=True,
                top_k=10,
                num_return_sequences=args.num_queries)
            
        for idx, qry in enumerate(outputs):
            qry_txt = tokenizer.decode(qry, skip_special_tokens=True)
            line = f'{doc_ids[idx]}\t{positions[idx]}\t{qry_txt}\n'
            ofile.write(line)

    logger.info('Finished all batches')
    ofile.close()
    doc_dataset.close()

if __name__ == "__main__":
    generate_queries()