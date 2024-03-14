from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 
app.secret_key = 'supersecretkey' 

def process_image(file):
    img = Image.open(file)
    gray_img = img.convert('L')
    target_size = (256, 256)
    resized_img = gray_img.resize(target_size)
    return resized_img

def save_image(img, filename, save_path):
    img.save(os.path.join(save_path, filename))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('file')
        save_option = request.form.get('save_option')

        if not files:
            flash('No file selected')
            return redirect(request.url)

        processed_image_paths = []
        for file in files:
            if file.filename == '':
                continue
            if file:
                filename = secure_filename(file.filename)
                if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    for filename in os.listdir(folder_path):
                        if filename.endswith(('.jpg', '.jpeg', '.png')):
                            img_path = os.path.join(folder_path, filename)
                            img = process_image(img_path)
                            if save_option == 'ask':
                                save_path = request.form.get('save_path')
                                save_image(img, filename, save_path)
                                processed_image_paths.append(os.path.join(save_path, filename))
                            else:
                                save_image(img, filename, app.config['DOWNLOAD_FOLDER'])
                                processed_image_paths.append(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
                else:
                    img = process_image(file)
                    if save_option == 'ask':
                        save_path = request.form.get('save_path')
                        save_image(img, filename, save_path)
                        processed_image_paths.append(os.path.join(save_path, filename))
                    else:
                        save_image(img, filename, app.config['DOWNLOAD_FOLDER'])
                        processed_image_paths.append(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))

        if processed_image_paths:
            return render_template('download_multiple.html', processed_image_paths=processed_image_paths)

    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
