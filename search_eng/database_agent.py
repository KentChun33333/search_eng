import time 
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import config

def run_thread(num_worker, func, **argv):
    # now return 
    executor = ThreadPoolExecutor(max_workers=num_worker)
    executor.submit(func, **argv)
    executor.shutdown(wait=False) 

class DataBaseSqlite3():
    def __init__(self, sqlite3_connstr='example.db'):
        print(sqlite3_connstr)
        self.conn = sqlite3.connect(sqlite3_connstr)
        self.cursor = self.conn.cursor()

    def __del__(self):
        '''
        this will be called if the object is destroied
        if we run if in another threading/progressing, if would act like 
        with + __exit__ operations 
        '''
        self.cursor.close()
        self.conn.close()

class URLTable(DataBaseSqlite3):
    # process insert or update 
    def __init__(self, sqlite3_connstr=config.forward_database):
        super().__init__(sqlite3_connstr=sqlite3_connstr)
        self.table_name = 'URLTable'
        self.init_table()

    def init_table(self):
        sql = f'''CREATE TABLE IF NOT EXISTS {self.table_name}
             (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
             url TEXT NOT NULL, 
             url_guid TEXT NOT NULL, 
             url_len INTEGER NOT NULL, 
             title_len INTEGER NOT NULL, 
             save_pth TEXT NOT NULL, 
             status INTEGER NOT NULL)'''
        self.cursor.execute(sql)
        self.conn.commit()

        for index_name in ['url_guid', 'url_len', 'title_len' ]:
            sql = f'''CREATE INDEX IF NOT EXISTS
                      {index_name} ON {self.table_name} ({index_name})'''
            self.cursor.execute(sql)
        self.conn.commit()
    
    def insert_record(self, url, url_guid, 
        url_len, title_len, save_pth, status):

        sql_string = f'''INSERT INTO "{self.table_name}"  
            (url, url_guid, url_len, title_len, save_pth, status) 
            SELECT "{url}", "{url_guid}", "{url_len}", 
            "{title_len}", "{save_pth}", "{status}" 
            WHERE NOT EXISTS ( SELECT 1 FROM "{self.table_name}" 
            WHERE url_guid == "{url_guid}" ) '''
        self.cursor.execute(sql_string)
        self.conn.commit()

    def get_to_indexier_top_K(self, numK):
        sql_string = f'''SELECT save_pth, url_guid, ID FROM "{self.table_name}" 
                             WHERE status != 1 Limit {numK}'''  
        self.cursor.execute(sql_string)
        self.conn.commit()
        return self.cursor.fetchall()
                        
    def udpate_status(self, url_guid):
        sql_string  = f'''
        UPDATE "{self.table_name}"
        SET status = 1 WHERE url_guid == "{url_guid}"
        '''
        self.cursor.execute(sql_string)
        self.conn.commit()

    def get_doc_url(self, doc_ids:list):
        doc_ids = [str(i) for i in doc_ids]
        sql_string = f'''SELECT url, ID FROM "{self.table_name}" 
                             WHERE ID in ({','.join(doc_ids)})'''  
        # print(sql_string)
        self.cursor.execute(sql_string)
        self.conn.commit()
        return self.cursor.fetchall()
