from abc import ABC
from typing import List
import numpy as np 

import gensim.models as g
import codecs
from scipy.spatial.distance import pdist

from collections import defaultdict, Counter
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from num2words import num2words
import re 
import config

class TxtPreprocess():
    def __init__(self, extra_stop_words: List[str] = None ):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        stop_words = set(stopwords.words("english"))

        new_words = [
                     "also", "iv"
                     ]

        self.stopword = stop_words.union(new_words)

    def _normalize(self, doc) ->'list of txt':
        #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ', doc)
        text = text.lower()
        
        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
        
        return text.split()
        
    def transform(self, doc: str)-> 'list of txt':
        res = {}
        list_txt = self._normalize(doc)

        lemm_text = [self.lemmatizer.lemmatize(word) for word in list_txt 
                     if not word in  self.stopword] 

        stem_text = [self.stemmer.stem(word) for word in list_txt 
                     if not word in  self.stopword] 

        res['stem'] = stem_text
        res['lemm'] = lemm_text
        return res

class FeatureExtrator(ABC):
    @classmethod
    def extrat_feat():
        raise NotImplementedError()
    
class KeyWordCountFrequency(FeatureExtrator):
    def __init__(self, ):
        pass 

    def extrat_feat(self, nor_txt_dict: dict) -> dict:
        doc_len = len(nor_txt_dict['stem']) 
        x_stem = Counter(nor_txt_dict['stem'])
        x_lemm = Counter(nor_txt_dict['lemm'])
        res = {}
        for k, v in x_lemm.items():
            term_frequency = float(x_lemm[k]/doc_len)
            res[k] = (x_lemm[k], term_frequency)
        return res 
    
class Doc2Vector300D(FeatureExtrator):
    def __init__(self, start_alpha=0.01, infer_epoch=500):
        self.model_pth = config.Doc2Vector300D_model_weight
        #inference hyper-parameters
        self.start_alpha = start_alpha
        self.infer_epoch = infer_epoch
        self.model = g.Doc2Vec.load(self.model_pth)
        #self.txt_preprocessor = TxtPreprocess()
    
    def extrat_feat(self, nor_txt_dict: dict) -> dict:
        #res = self.txt_preprocessor.transform(doc)
        x_stem = nor_txt_dict['stem']
        x_lemm = nor_txt_dict['lemm']
        y_stem = self.model.infer_vector(x_stem, alpha=self.start_alpha, 
                              steps=self.infer_epoch)
        y_lemm = self.model.infer_vector(x_lemm, alpha=self.start_alpha, 
                              steps=self.infer_epoch)
        nor_txt_dict['docvec_stem'] = y_stem
        nor_txt_dict['docvec_lemm'] = y_lemm
        return nor_txt_dict
        