import pickle
from run_model_indexier import TrieNodeDB
from model_indexier.txt_preprocess import TxtPreprocess
from database_agent import URLTable
from collections import Counter
import config 

class Querier():
    def __init__(self):
        self.database = pickle.load(open(config.inverted_database, 'rb'))
        self.txt_agent = TxtPreprocess()
        
    def get_candidates(self, query: 'txt'):
        res_q = self.txt_agent.transform(query)
        res_q = res_q['lemm']
        # similarity to correct the word

        # print('res_q: ', res_q)
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
        doc_ids = self.get_candidates(query)
        urltable = URLTable()
        return urltable.get_doc_url([i[0] for i in doc_ids])
