from model_indexer import Doc2Vector300D
import config 
import pickle
from scipy.spatial.distance import squareform, pdist
import numpy as np 

class RankModelDocVec():
    def __init__(self):
        # load object or connect with db if we use db 
        self.doc_vec_db = pickle.load(open(config.doc_vec_db , 'rb'))
        self.doc2vec_agent = Doc2Vector300D()

    def rank_candidates(self, nortextdict: dict, doc_ids:list, dist_mode='cosine'):
        '''
          nortextdict: after txt preprocess 
        '''
        query_vec = self.doc2vec_agent.extrat_feat(nortextdict) # Dim = (300, )
        query_vec  = query_vec['docvec_lemm']

        candidate_vec = [self.doc_vec_db[i] for i in doc_ids] 
        pair_matric = np.vstack([query_vec] + candidate_vec)
        # 1D array of similarity, get rid of self-self similarity 
        print(dist_mode)
        distance = squareform(pdist(pair_matric, metric=dist_mode))[0][1:]
        # sort index from low to high
        order_index =  list(np.argsort(distance))
        return [doc_ids[i] for i in order_index]

# def pairwise_cos_sim(matrix):
#     # matrix
#     similarity = np.dot(matrix, matrix.T)
#     # squared magnitude of preference vectors (number of occurrences)
#     square_mag = np.diag(similarity)
#     # inverse squared magnitude
#     inv_square_mag = 1 / square_mag
#     # if it doesn't occur, set it's inverse magnitude to zero (instead of inf)
#     inv_square_mag[np.isinf(inv_square_mag)] = 0
#     # inverse of the magnitude
#     inv_mag = np.sqrt(inv_square_mag)
#     # cosine similarity (elementwise multiply by inverse magnitudes)
#     cosine = similarity * inv_mag
#     cosine = cosine.T * inv_mag
#     return cosine