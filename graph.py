import functools
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify,json
)
from werkzeug.security import check_password_hash, generate_password_hash

#from MVP.db import get_db

bp = Blueprint('graph', __name__, url_prefix='/graph')
@bp.route('/graph',methods=('GET','POST'))
def graph():
    return render_template('graph/test.html')
#def generate_new_bar():
  #  path = os.getcwd()+"/graph/bar.html"
    #new_bar = open(path)
@bp.route('/matrix',methods=('GET','POST'))
def matrix():
    #f = open('matrix.html','w')
    path = os.getcwd()+'/MVP/templates/graph'
    complete_name = os.path.join(path,"matrixt.html")
    file1 = open(complete_name,'w')
    toFile = "test_matrix"
    file1.write(toFile)
    file1.close()
    return render_template('graph/matrixt.html')
@bp.route('/pruned',methods=('GET','POST'))
def pruned():
    return render_template('graph/pruned.html')
@bp.route('/return_string',methods=('GET','POST'))
def return_string():

    d = {'test0':10989,'test1':222}
    content = request.get_json()
    print(type(content))
    return jsonify(d)

