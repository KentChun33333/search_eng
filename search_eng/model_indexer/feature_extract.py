from abc import ABC
from gensim.models import Doc2Vec
from collections import defaultdict, Counter
import config

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
        self.model = Doc2Vec.load(self.model_pth)
    
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
        