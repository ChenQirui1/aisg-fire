from flask import Flask, Response, render_template, redirect, flash, request,url_for
import os

# from flask import Request
from werkzeug.utils import secure_filename

import cv2
import yaml
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath("uploads")
video = cv2.VideoCapture(0)

@app.route("/")
def hello():
    
    return render_template('home.html')
 
@app.route('/upload_video', methods=['GET','POST'])
def upload_video():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(url_for('camera_test'))
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            #flash('No selected file')
            return redirect(url_for('camera_test'))
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('camera_test', name=filename))


@app.route('/upload_image', methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(url_for('camera_test'))
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            #flash('No selected file')
            return redirect(url_for('camera_test'))
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('camera_test', name=filename))

@app.route('/camera')
def camera_test():
    return render_template('capture.html')

@app.route('/display/<incident_id>')
def display_content(incident_id):
    
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,debug=True)
    
    
# with open('pipeline_config.yml') as f:
    #     try:
    #         os.system("peekingduck run")
    #         #print(dict)
    #     except:
    #         print("Fail")
            
            
    # os.system("peekingduck run")
        
    # return "hello_world"