# 1. Project Introduction 

A simple search system that mostly written in python. Typically, search/recommend system would including several key components (1) Web Crawler (2) Indexing (3) Recall model/mechanism (4) Ranking model (5) Query Web-Interface. Since lacking of training data, I don't have rank model at the moment. 

<img src="doc\system_flow.png" alt="image-20200924000928319" style="zoom:75%;" />



## 1.1 Web Crawler 

- Using *selenium* and *beautifulsoup4* to fetch the data from https://stackoverflow.com that mostly related to database. In addition, currently only crawling the title as document for storage concerns. Using *sqlite3* as forward-database. 

  ![image-20200923225222753](doc\forward_db.png)

  

## 1.2 Indexer

- Using *nltk* and *gensim* to do the text normalization, stemming, lemmatization and doc2vec. 

- Using a customized object as inverted (index) database. For real applications, we can chose *leveldb*, *dynamodb* or *rockdb*. The customized object is basically a k-value object with the optimization that applies tire-tree on inverted index. 

  | index (key word) | Value                            |
  | ---------------- | -------------------------------- |
  | sql              | [ (doc_id, term_frequency), ...] |
  | database         | [ (doc_id, term_frequency), ...] |

- There are many advanced efficient index way, and for vector-database the indexing method often consisted of clustering and quantization methods.

## 1.3 Recall Model / Mechanism

- Here using traditional bool-query.  It could be further enhance with term-frequency or even a model to recall the candidates.

## 1.4 Query Interface

- Using Flask and Jinja template with bootstrap UI framework. 

  ![image-20200922102507130](doc\demo.gif)



# 2. Usage Flow

- install the requirement packages 
- install chrome driver for selenium in data/web_driver
  - It should align with the config.py
- python **run_web_crawler.py** 
  - It would create a forward database and storing blob in local machine.
- python **run_model_indexier.py** 
  - It would run text normalization and then build the inverted-index object. 
- python **run_query_interface.py**
  - It would run a flask server on localhost:5000. 
- Config File 
  - forward_database = *r*'data/sqldb/example.db'
  - inverted_database = *r*'data/sqldb/inverted_key_word_db.pkl'
  - Doc2Vector300D_model_weight = *r*"data/model/doc2vec.bin"



# 3. Result Comparison

Current result just using traditional bool query, and not counting lots features like voting, user persona, content of question, and content of reply answers. 

|                                             |                                           |
| ------------------------------------------- | ----------------------------------------- |
| ![image-20200922102558811](doc\image_2.png) | ![image-20200922102558811](doc\image.png) |




# 4. Further Improvement 
- There are lots of things we could improve on and play with:
  - **Model-based recall mechanism**:  Personally, I also build the vectors database of title-text, however not index it yet for fast-read. There are some ways to index the dense-vector database via some clustering or quantization methods. I would like to try some of them after more understanding of them.  Also, I am not sure how much improvement would it bring to the overall performance.
  - **Ranking model**: Since having no feasible dataset to train on, there is no ranking model here. However, the ranking/suggestion model is definitely one of key component of the search/recommend system.  
  - **Distributed Storage**: we definitely can shading the database, both on forward-database and inverted database.
  - **Crawling for more content: ** Due to storage limitations, I treat the title of the document as entire document. However, we could also crawling and parsing content as well.
  - **Advanced Indexing method: ** if the data is large, we may need to do some compression on index. In addition, for dense vector-based search/recommend system, we may need to using clustering/product quantization plus multi-index method to index the database. There are several famous method like Non-Orthogonal Inverted Multi-Index or IVFADC.
