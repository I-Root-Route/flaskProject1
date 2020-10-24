import os
import csv
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
import glob

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = BASE_DIR + '/uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('csv.html')


@app.route('/show_csv', methods=['GET', 'POST'])
def show_csv():
    if request.method == 'POST':
        send_data = request.files['send_data']
        if send_data and allowed_file(send_data.filename):
            filename = secure_filename(send_data.filename)
            send_data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            f = open(BASE_DIR + '/uploads/' + filename, 'r')
            f_reader = csv.reader(f)
            result = list(f_reader)

            return render_template('csv.html', result=result)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    if request.method == 'POST':
        import dataprocessing
        dataprocessing
        is_processed_file = True
        # is_processed_file = os.path.exists(BASE_DIR + '/processed/X_test_processed.csv')
        return render_template('csv.html', exist=is_processed_file)


@app.route('/get_final_result', methods=['GET', 'POST'])
def get_final_result():
    if request.method == 'POST':
        import prediction
        prediction
        isfile = True
        # isfile = os.path.exists(BASE_DIR + '/final_result/final_result.csv')
        return render_template('csv.html', isfile=isfile)


@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
    # upload_path = glob.glob(BASE_DIR + '/uploads/*.csv')[0]
    # processed_path = glob.glob(BASE_DIR + '/processed/X_test_processed.csv')[0]
    if request.method == 'POST':
        # os.remove(upload_path)
        # os.remove(processed_path)
        return send_from_directory(
            directory=BASE_DIR + '/final_result',
            filename='final_result.csv',
            as_attachment=True,
            attachment_filename='final_result.csv'
        )


if __name__ == '__main__':
    app.debug = True
    app.run()
