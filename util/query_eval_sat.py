#!/usr/bin/python3


class QueryComparitor():

    def __init__(self):
        self.MSMARCO_DOCS = "/home/ubuntu/efs/data/msmarco_docs/msmarco-docs.tsv"
        self.MSMARCO_QUERIES = "/home/ubuntu/efs/data/msmarco_docs/msmarco-doctrain-queries.tsv"
        self.TRESPI_QUERIES = "/home/ubuntu/neural_info_retrieval/TRESPI/saved_data/all_queries7Jul.tsv"
        self.msmarco_docs = {}
        self.msmarco_queries = {}
        self.trespi_queries = {}
        self.master_doclist = []

    def readMSMarcoDocs(self):
        fh = open(self.MSMARCO_DOCS,"r")
        for i, line in enumerate(fh):
            document_id, link, query, text = line.split('\t',maxsplit=4)
            self.msmarco_docs[document_id] = set(query.split())

    def readMSMarcoQueries(self):
        fh = open(self.MSMARCO_QUERIES,"r")
        for i, line in enumerate(fh):
            document_id, query = line.split('\t',maxsplit=2)
            document_id = "D" + document_id
            self.msmarco_queries[document_id] = set(query.split())

    def readTRESPIQueries(self):
        fh = open(self.TRESPI_QUERIES,"r")
        for i, line in enumerate(fh):
            document_id, passage, query = line.split('\t',maxsplit=3)
            if document_id in self.trespi_queries:
                self.trespi_queries[document_id] = set(query.split()).union(self.trespi_queries[document_id])
            else:
                self.trespi_queries[document_id] = set(query.split())

    def deriveMasterDoclist(self):
        self.master_doclist = set(list(self.msmarco_docs.keys()) + list(self.msmarco_queries.keys()) + list(self.trespi_queries.keys()))

    def analyze(self):

        ids_common_queries = len(set(self.msmarco_docs.keys()).intersection(set(self.msmarco_queries.keys())))
        ids_common_trespi = len(set(self.msmarco_docs.keys()).intersection(set(self.trespi_queries.keys())))

        for document_id in list(self.master_doclist):
            terms_docs = len(self.msmarco_docs[document_id]) if document_id in self.msmarco_docs else 0
            terms_queries = len(self.msmarco_queries[document_id]) if document_id in self.msmarco_queries else 0
            terms_trespi = len(self.trespi_queries[document_id]) if document_id in self.trespi_queries else 0
            trespi_int_docs = self.query_intersect(document_id,self.msmarco_docs,self.trespi_queries)
            trespi_int_queries = self.query_intersect(document_id,self.msmarco_queries,self.trespi_queries)
            trespi_comp_docs = self.query_complement(document_id,self.msmarco_docs,self.trespi_queries)
            trespi_comp_queries = self.query_complement(document_id,self.msmarco_queries,self.trespi_queries)
            yield((document_id,terms_docs,terms_queries,terms_trespi,trespi_int_docs,trespi_int_queries,trespi_comp_docs,trespi_comp_queries))

    def query_intersect(self,doc,a,b):
        terms_a = a[doc] if doc in a else set()
        terms_b = b[doc] if doc in b else set()
        return(len(terms_a.intersection(terms_b)))

    def query_complement(self,doc,a,b):
        terms_a = a[doc] if doc in a else set()
        terms_b = b[doc] if doc in b else set()
        return(len(terms_a.union(terms_b).difference(terms_a)))

    def buildSets(self):
        self.readMSMarcoDocs()
        self.readMSMarcoQueries()
        self.readTRESPIQueries()
        self.deriveMasterDoclist()



x = QueryComparitor()
x.buildSets()

for term_tuple in x.analyze():
    print(term_tuple)


