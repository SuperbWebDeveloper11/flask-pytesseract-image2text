import os
from flask import Flask, render_template, request
from PIL import Image
import pytesseract


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)


# Read an image and extract text from it
def image_to_text(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img) 
    return text


# Return True if file is allowed and False if not
def check_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home page
@app.route('/')
def home_page():
    return render_template('index.html')


# Upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():

    if request.method == 'POST':

        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and check_file_extension(file.filename):
            # now we user our function to extract text from the image
            extracted_text = image_to_text(file)

            return render_template('upload.html',
                msg='Successfully processed',
                extracted_text=extracted_text)

    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()

