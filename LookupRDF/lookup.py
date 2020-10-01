'''
Created on Jun 17, 2020

@author: XHG3
'''
from ConnectRedis import r
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__, template_folder='./templates',static_folder="",static_url_path="")


@app.route('/')
def index():
    return render_template('keyword.html')

@app.route('/lookup',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        keyword = request.form['nm']
        print('keyword typing:', keyword)
        res = r.lrange(keyword, 0, -1)
        return render_template("result.html",keyword=keyword,result = res)
#         return  ('welcome %s' % res)
    else:
        keyword = request.args.get('nm')
        res = r.lrange(keyword, 0, -1)
        return render_template("result.html",keyword=keyword,result = res)
#         return  ('welcome %s' % res)

if __name__ == '__main__':
    app.run(debug = True)