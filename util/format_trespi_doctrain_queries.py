#!/home/ubuntu/anaconda3/envs/python3/bin/python3

# wade.holmes@berkeley.edu

class TRESPIDoctrainFormatter:

    def __init__(self,query_input,query_output,stopwords_file):
        self.query_input_file = query_input
        self.query_output_file = query_output

        self.stopwords = []
        with open(stopwords_file,"r") as stopwords_dictionary:
            for stopword in stopwords_dictionary:
                self.stopwords.append(stopword.rstrip())
        

    def trespiQuery(self):
        passage_history = []
        with open(self.query_input_file,"r") as query_source:
            for query_line in query_source:
                document_id, passage_num, query_terms = query_line.rstrip().split('\t')
                passage_id = "{}:{}".format(document_id,passage_num)
                if passage_id not in passage_history:
                    passage_history.append(passage_id)
                    yield((document_id,passage_num,query_terms))

    def formatDoctrain(self,data_tuple):
        body_text = "hold for body text"
        query_part = data_tuple[2]
        recall_part = {key: 1 for key in self.formatTermRecall(data_tuple[2])}
        doc_part = {"position": data_tuple[1], "id": data_tuple[0], "title": body_text}
        doctrain_json = {"query": query_part, "term_recall": recall_part, "doc": doc_part}
        return(doctrain_json)

    def formatTermRecall(self,query_terms):
        term_recall_list = []
        for term in query_terms.split():
            if term not in self.stopwords:
                term_recall_list.append(term)
        return(term_recall_list)



source = '/home/ubuntu/neural_info_retrieval/TRESPI/saved_data/all_queries7Jul.tsv'
stopwords = '/home/ubuntu/efs/trainvol/trespi/DeepCT/data/marco/stopwords.txt'

dest = None
formatter = TRESPIDoctrainFormatter(source,dest,stopwords)
for line in formatter.trespiQuery():
    print(formatter.formatDoctrain(line))
