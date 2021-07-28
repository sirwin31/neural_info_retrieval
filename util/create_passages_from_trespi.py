#!/home/ubuntu/anaconda3/envs/python3/bin/python3

class PassageCreator:

    def __init__(self, trespi_datafile):

        self.input_filename = trespi_datafile

    def createPassageIDs(self):

        keylist = []
        with open(self.input_filename,"r") as fh:
            for line in fh:
                doc_id,passage_id,passage_text = line.split('\t',3)
                passage_id = self.formatPassageID(doc_id,passage_id)
                if passage_id not in keylist:
                    keylist.append(passage_id)
        return(keylist)


    def createPassageByID(self, key):
        passage = str()
        with open(self.input_filename,"r") as fh:
            for line in fh:
                doc_id,passage_id,passage_text = line.split('\t',3)
                passage_id = self.formatPassageID(doc_id,passage_id)
                if passage_id == key:
                    if len(passage) > 0:
                        passage = passage + ". " + passage_text.trim()
                    else:
                        passage = passage_text.trim()
        return(passage)

    def formatPassageID(self,doc_id,passage_id):
        return(doc_id + "_" + str(passage_id).zfill(3))


trespi_outfile = "/home/ubuntu/neural_info_retrieval/TRESPI/saved_data/all_queries7Jul.tsv"

pc = PassageCreator(trespi_outfile)

for passage_id in pc.createPassageIDs():
    passage_text = pc.createPassageByID(passage_id)
    print(passage_id + "\t" + passage_text)



