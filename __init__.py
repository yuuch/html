import os
from flask import Flask 
from flask import render_template,request,redirect,url_for,flash
from werkzeug.utils import secure_filename
import pickle
def create_app(test_config=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER = os.getcwd()+'/MVP/upload_files'
    )
    #os.makedirs(os.path.join(app.instance_path,'upload_files'), exist_ok=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    @app.route('/',methods=['GET','POST'])
    def index():
        return render_template('base.html')

    @app.route('/upload_metadata',methods=['GET','POST'])
    def upload_metadata():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file :
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                metadata_dict = {'metadata_filename':filename}
                with open('MVP/pickles/metadata_filename.pickle','wb') as f:
                    pickle.dump(metadata_dict,f)
                return redirect(url_for('upload_tree'))
        return render_template('upload_metadata.html')

    @app.route('/upload_tree',methods=['GET','POST'])
    def upload_tree():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file :
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                tree_dict = {'tree_filename':filename}
                with open('MVP/pickles/tree_filename.pickle','wb') as f:
                    pickle.dump(tree_dict,f)
                return redirect(url_for('upload_taxonomy'))
        return render_template('upload_tree.html')
    @app.route('/upload_taxonomy',methods= ['GET','POST'])
    def upload_taxonomy():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file :
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                taxonomy_dict = {'taxonomy_filename':filename}
                with open('MVP/pickles/taxonomy_filename.pickle','wb') as f:
                    pickle.dump(taxonomy_dict,f)
                return redirect(url_for('upload_feature_table'))
        return render_template('upload_taxonomy.html')
            

    @app.route('/upload_feature_table',methods=['GET','POST'])
    def upload_feature_table():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file :
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                feature_table_dict = {'feature_table_filename':filename}
                with open('MVP/pickles/feature_table_filename.pickle','wb') as f:
                    pickle.dump(feature_table_dict,f)
                return redirect(url_for('index'))
        return render_template('upload_feature_table.html')

    @app.route('/phylogenetic_view',methods=['GET', 'POST'])
    def phylogenetic_view():
        if request.method == 'POST':
            return redirect(url_for('index'))
        return render_template('phylogenetic_view.html')

    @app.route('/multi_target_view',methods=['GET', 'POST'])
    def multi_target_view():
        if request.method == 'POST':
            return redirect(url_for('index'))
        return render_template('multi_target_view.html')
        
    @app.route('/optimization',methods=['GET', 'POST'])
    def optimization():
        if request.method == 'POST':
            return redirect(url_for('index'))
        return render_template('optimization.html')
        








    from . import graph
    app.static_file='static'
    app.register_blueprint(graph.bp)
    return app
