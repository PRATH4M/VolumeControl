from flask import Flask, render_template, request, send_file
import os
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)

def process_folders(folder_paths, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Folder', 'Filename'])  # Write header
        
        for folder_path in folder_paths:
            folder_name = os.path.basename(folder_path)
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    if file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.jpeg'):
                        new_file_name = f"{folder_name}_{file_name}"
                        csv_writer.writerow([folder_name, new_file_name])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'folder1' not in request.files or 'folder2' not in request.files:
        return 'Missing folder part'

    folder1 = request.files['folder1']
    folder2 = request.files['folder2']

    if folder1.filename == '' or folder2.filename == '':
        return 'No selected folder'

    folder1_path = os.path.join(app.root_path, secure_filename(folder1.filename))
    folder2_path = os.path.join(app.root_path, secure_filename(folder2.filename))

    os.makedirs(folder1_path, exist_ok=True)
    os.makedirs(folder2_path, exist_ok=True)

    folder1.save(folder1_path)
    folder2.save(folder2_path)

    return render_template('save_as.html', folder1=folder1.filename, folder2=folder2.filename)

@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    csv_file_path = os.path.join(app.root_path, f'{filename}.csv')
    process_folders([os.path.join(app.root_path, secure_filename(request.form['folder1'])), os.path.join(app.root_path, secure_filename(request.form['folder2']))], csv_file_path)
    return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
