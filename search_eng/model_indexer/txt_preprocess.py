from typing import List
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
