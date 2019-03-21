# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory, render_template, jsonify, redirect
from werkzeug.utils import secure_filename
import shutil
from datetime import timedelta
from area_cal import cal


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd() + "/uploaded_images"
app.config['RESULT_FOLDER'] = os.getcwd() + "/results"
# app.config['SEND_FILE_MAX_DEFAULT'] = timedelta(seconds=1)
# app.config['ERMANENT_SESSION_LIFETIME'] = timedelta(seconds=1)
# app.config['MAX_CONTENT_LENGTH'] = 8 * 256 * 256


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>', methods=['POST', 'GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/result/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'],
                               filename)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


filename_upload = ""


@app.route('/uploadImg', methods=['POST'])
def upload_file():
    shutil.rmtree('./uploaded_images')
    os.mkdir('uploaded_images')
    file = request.files['file']

    if file and allowed_file(file.filename):
        global filename_upload
        filename_ = secure_filename(file.filename)
        # filename = file.filename
        filename_upload = filename_

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_))
        print "file path to show:", os.path.join(app.config['UPLOAD_FOLDER'], filename_)
        file_url = url_for('.uploaded_file', filename=filename_)

        return jsonify(name=filename_, file_url=file_url)
        # return redirect(url_for('uploaded_file', filename=file_url))


@app.route('/predictImg', methods=['POST'])
def predict_img():
    # request.values("alpha")
    # print form_
    # ################
    seg = filename_upload.split('_segmentation')
    print "Yuuav upload image name: {}".format(filename_upload)
    img_name = ''.join(seg)
    print "image name json url: {}".format(img_name)
    alpha = request.form.get("alpha")
    print "flask_parameter alpha:{}".format(alpha)
    Area, Cir = cal.main(img_name, alpha)  # alpha is the coefficient: 1 pixel length = alpha m

    return jsonify(name=img_name, area=Area, cir=Cir)


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)
