#!/home/ubuntu/anaconda3/envs/python3/bin/python3

trespi_outfile = "/home/ubuntu/neural_info_retrieval/TRESPI/saved_data/all_queries7Jul.tsv"

def formatPassageID(doc_id,passage_id):
    return(doc_id + "_" + str(passage_id).zfill(3))

current_passage_id = None
passage_body = str()
indexer = 0

with open(trespi_outfile,"r") as fh:
    for line in fh:
        doc_id,passage_id,passage_text = line.split('\t',3)
        passage_id = formatPassageID(doc_id,passage_id)

        passage_text = passage_text.rstrip()

        if current_passage_id != passage_id:
            if current_passage_id is not None:
                #print(current_passage_id + "\t" + passage_body)
                print(str(indexer) + "\t" + passage_body)
                indexer += 1
            passage_body = passage_text
            current_passage_id = passage_id
        else:
            passage_body = passage_body + ". " + passage_text




