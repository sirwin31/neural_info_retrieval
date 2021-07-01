import argparse
import sys

import torch
import torch.utils.data
import transformers

sys.path.append('/home/ubuntu/TRESPI')
import doc_dataset as ds

MODEL_NAME = 'castorini/doc2query-t5-base-msmarco'

# Set up command-line arguments.
desc = ('Uses the doc2query-T5 model to generate queries from '
        'source documents.')
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('path', help='Path to TSV file with MS Marco documents')
parser.add_argument('output-file', help='Path to output file')
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
                         ' Default is to use all queries in docs file')
parser.add_argument('--qry-len', type=int, default=64,
                    help='Max length of generated queries')
parser.add_argument('--batch-size', type=int, default=16,
                    help='Batch size for inputs to doc2query-T5')


def generate_queries():
    args = parser.parse_args()

    # Prepare the source documents
    doc_dataset = ds.DocDataset(args.path,
                                min_len=args.psg_min,
                                tgt_len=args.psg_tgt,
                                max_len=args.psg_max,
                                max_passages=args.max_psg_in)
    doc_loader = torch.utils.data.DataLoader(
        doc_dataset,
        batch_size=args.batch_size
    )

    # Tokenizer will convert model output back to text
    tokenizer = transformers.T5Tokenizer.from_pretrained(MODEL_NAME)

    # Create model and send to GPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = transformers.T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    model.to(device)

    # Query Generation Loop
    for batch in doc_loader:
        # Setup model inputs
        doc_ids = batch[0]
        positions = batch[1]
        input_ids = batch[2].to(device)  # To GPU
        mask = batch[3].to(device)       # To GPU

        # Run a batch through T5 model
        outputs = model.generate(
            input_ids = input_ids,
            attention_mask = mask,
            max_length=args.qry_len,
            do_sample=True,
            top_k=10,
            num_return_sequences=args.num_queries)

        # Display output
        print('Passages=======')
        for idx, doc_id in enumerate(doc_ids):
            print(doc_id, positions[idx],
                 tokenizer.decode(input_ids[idx], skip_special_tokens=True))
        print()

        print('Queries======')
        for qry in outputs:
            qry_txt = tokenizer.decode(qry, skip_special_tokens=True)
            print(qry_txt)

    doc_dataset.close()

if __name__ == "__main__":
    generate_queries()