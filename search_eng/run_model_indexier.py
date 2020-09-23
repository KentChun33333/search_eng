
from model_indexier.txt_preprocess import (TxtPreprocess, 
KeyWordCountFrequency, Doc2Vector300D) 

from database_agent import URLTable

from concurrent.futures import ThreadPoolExecutor
import pickle, collections, os
from tqdm import tqdm 
import config 


# trie tree as index and to storage for keyword 
class TrieNodeDB:
    def __init__(self):
        self.children = collections.defaultdict(TrieNodeDB)
        self.val = []
    
    def update(self, key, value):
        # if the key is in tri, updated value 
        cur_node = None
        cur_chid = self.children
        for i in key:
            if i not in cur_chid:
                cur_chid[i] = TrieNodeDB()
            cur_node = cur_chid[i]
            cur_chid = cur_node.children
        
        # to the end 
        if not cur_node.val:
            cur_node.val = [value]
        else : # already have 
            if value not in cur_node.val:
                cur_node.val.append(value)

    def soft_get(self, key):
        # a relaxiation of the get 
        # if the match 80% of word, will return 
        res = []
        M = int(0.8*len(key))
        cur_chid = self.children
        for ind, item in enumerate(key):
            if not item in cur_chid:
                break
            cur_node = cur_chid[item]
            cur_chid = cur_node.children
            if ind >= M-1 :
                res += cur_node.val
        return res 
            
    def get(self, key):
        cur_node = None
        cur_chid = self.children
        for ind, item in enumerate(key):
            if not item in cur_chid:
                return []
            cur_node = cur_chid[item]
            cur_chid = cur_node.children
        return cur_node.val       


# to storage for vector-space-model
# the key is how to index it so that we can retrival fast 
# 
def get_inverted_key_word_db():
    pth = config.inverted_database
    if not os.path.exists(pth):
        return TrieNodeDB()
    else:
        return pickle.load(open(pth, 'rb'))
    
def get_doc_vec_db():
    # simple dictionary 
    pth = 'data/sqldb/doc_vec_db.pkl'
    if not os.path.exists(pth):
        return {}
    else:
        return pickle.load(open(pth, 'rb'))


def run_thread(num_worker, func, **argv):
    # now return 
    executor = ThreadPoolExecutor(max_workers=num_worker)
    executor.submit(func, **argv)
    executor.shutdown(wait=False) 


def main():
    url_table = URLTable()
    txt_processor = TxtPreprocess()
    key_word = KeyWordCountFrequency()
    doc_vec = Doc2Vector300D()

    inverted_key_word_db = get_inverted_key_word_db()
    doc_vec_db = get_doc_vec_db()
    ind = 0 
    minibatch_size = 10000
    genobj = url_table.get_to_indexier_top_K(minibatch_size)
    while len(genobj)>0:
        print(f'minibatch {ind}')
        for save_pth, url_guid, doc_id in tqdm(genobj):
            doc = pickle.load(open(save_pth, 'rb')) 
            nor_doc_dict = txt_processor.transform(doc)
            key_word_resdict = key_word.extrat_feat(nor_doc_dict)
            doc_vec_resdict = doc_vec.extrat_feat(nor_doc_dict)
                    
            # key_word_resdict  word : (repeatence, term-frequency) 
            # for ex : {'postgr': (1, 0.2), 'sql': (1, 0.2),}
            
            for word, value in key_word_resdict.items():
                repeatence, term_freq = value 

                inverted_key_word_db.update(
                    word, (doc_id, repeatence, round(term_freq, 6)))

            # update doc id 
            doc_vec_db.update(
                {doc_id: doc_vec_resdict['docvec_lemm']})
             
            url_table.udpate_status(url_guid)
            ind+=1
        pickle.dump(inverted_key_word_db, open(config.inverted_database, 'wb'))
        pickle.dump(doc_vec_db, open(config.inverted_doc_vec_db, 'wb'))
        genobj = url_table.get_to_indexier_top_K(minibatch_size)


if __name__ == '__main__':
    main()