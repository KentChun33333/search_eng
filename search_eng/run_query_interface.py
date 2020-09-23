import os
from flask import Flask, render_template
from flask import request
from web_query.queryer import Querier, TrieNodeDB

app = Flask(__name__, template_folder='web_query/front')
query_agent = Querier()

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        try:
            res = request.form['query']
            print(res)
        except:
            errors.append(
                "Unable to get result. Please make sure it's valid and try again."
            )
            return render_template('/index.html', errors=errors)
        if res:
            # text processing
            print('query: ', res)
            search_res = query_agent.get_url(res)
            search_res = [i[0] for i in search_res]
            search_title = [i.split('/')[-1].replace('-', ' ') for i in search_res]
            results = dict(
                        table = list(zip(range(len(search_res)), search_res, search_title)), 
                        query = res
                       )
        else:
            results = dict(
                        table = [('NA', 'NA')], 
                        query = 'NA'
                       )
    #  SQLite objects created in a thread can only be used in that same thread
    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()