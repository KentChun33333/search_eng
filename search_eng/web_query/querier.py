import pickle
from run_model_indexer import TrieNodeDB
from model_indexer import TxtPreprocess
from database_agent import URLTable
from model_rank import RankModelDocVec
from collections import Counter
import config 

class Querier():
    def __init__(self):
        self.database = pickle.load(open(config.inverted_database, 'rb'))
        self.txt_agent = TxtPreprocess()
        self.rank_agent = RankModelDocVec()
        
    def get_candidates(self, nortextdict: dict):
        res_q = nortextdict['lemm']
        res = []
        for key_word in res_q:
            res += [i[0] for i in self.database.get(key_word)]

        if len(res) < 1:
            for key_word in res_q:
                res += [i[0] for i in self.database.soft_get(key_word)]
        counter = Counter(res) 
        y = counter.most_common(50)
        return y

    def get_url(self, query:'txt'):
        nortextdict = self.txt_agent.transform(query)
        doc_ids = self.get_candidates(nortextdict) 
        # doc_ids = [(docid, number of match words), ...]
        doc_ids = [i[0] for i in doc_ids] # list 
        # ranking by vec 
        # euclidean, minkowski, cosine, seuclidean
        doc_ids = self.rank_agent.rank_candidates(nortextdict, doc_ids, 
                                                  dist_mode='euclidean')
        urltable = URLTable()
        return urltable.get_doc_url(doc_ids)