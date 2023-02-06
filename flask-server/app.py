from flask import Flask, Response, render_template, redirect, flash, request,url_for
import os
import json
import yaml
from datetime import datetime
from tinydb import TinyDB, Query
from re import match
import utils
import subprocess

# from flask import Request
from werkzeug.utils import secure_filename
import yaml
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath("static/uploads")
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = TinyDB('data.json')

@app.route("/")
def hello():
    data = utils.read_json("incidents.json")
    print(data['incidents'])
    return render_template('home.html',incidents = data['incidents'])

@app.route("/admin")
def admin():
    data = utils.read_json("incidents.json")
    return render_template('admin.html',incidents = data['incidents'])


#related to post.html
@app.route("/view-post/<incident_id>")
def view_post(incident_id):
    Posts = Query()
    posts = db.search(Posts.incident_id == incident_id)
    print(posts)
    return render_template('post.html',posts=posts)

@app.route("/get-video/<filename>")
def get_media(filename):
    media_path = os.path.join(app.config['UPLOAD_FOLDER'], f'/prediction/{filename}')
    return media_path



@app.route("/success",methods=['GET','POST'])
def success():
    return render_template('success.html')

# @app.route('/upload_video', methods=['GET','POST'])
# def upload_video():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             #flash('No file part')
#             return redirect(url_for('success'))
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             #flash('No selected file')
#             return redirect(url_for('success'))
#         if file:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('success'))

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return "Upload Error. Please Try Again"
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return "Upload Error. Please Try Again"
        if file:
            #file upload/prediction handlers
            filename = secure_filename(file.filename)
            media_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pred_path = os.path.abspath("static")
            data = dict(request.form)
            data["create_time"] = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
            file.save(media_path)
            utils.modify_yaml(media_path,data["media_type"])
            #os.chdir(os.path.abspath("../peeking-duck"))
            #print("Path Changed to peeking-duck")
            
            #print(peekingduck_path)
            
            #os.system("peekingduck run")
            # os.chdir(os.path.abspath("../flask-server"))
            # print("Path returned to flask-server")
            peekingduck_path = os.path.abspath("../peeking-duck")
            p = subprocess.Popen("peekingduck run", shell=True, cwd=peekingduck_path)
            p.wait()
            
            #create document
            data["filename"] = filename
            data['pred_filename'] = utils.retrieve_pred_filename(filename,pred_path)
            #print(data)
            db.insert(data)
            
        return render_template('success.html')

@app.route('/capture')
def capture():
    inc_id  = request.args.get('incident_id', None)
    media_type  = request.args.get('media', None)
    return render_template('form.html',media_type=media_type,incident_id=inc_id)


if __name__ == '__main__':
    app.run(threaded=True,debug=False,host="0.0.0.0")