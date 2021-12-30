import keras
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
import os

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from keras.preprocessing import image
from werkzeug.utils import secure_filename

# This code works only for photos with jpg and png format
ALLOWED_EXTENSIONS = set(['jpg', 'png'])

# We have dictionary to map our models result to label
label_to_ids = {0:"camera", 1:"laptop", 2:"mobile", 3:"tv"}

app = Flask(__name__)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'static/uploads/' 

# This method is for loading image and we should give this loaded img_tensor to our model
def load_image(img_path):
    img = image.load_img(img_path, target_size=(256, 256))
    img_tensor = image.img_to_array(img) 
    img_tensor = np.expand_dims(img_tensor, axis=0)      
    img_tensor /= 255.
    return img_tensor

# This method does whole prediction, it call method for load image, predicts result and returns it. 
# My threshold is 70%, after testing dozen images I guessed that this can me good threshold so if prediction is less then 70%,
# model will return -1, this means that model can't predict anything and this photo is undefined
def model_prediction(img, model):
    image = load_image(img)
    prediction = model.predict(image)
    if np.max(prediction) < 0.7:
        prediction = -1
    return prediction # return list of probabilities

# This method just checks filenames and extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# When get request is sent, index.html is opened
@app.route('/', methods = ['GET'])
def main():
    return render_template('index.html')

# Here we have logic for post request
@app.route('/', methods = ['POST'])
def upload_image():
    image_paths = []
    if 'files[]' not in request.files:
        flash('No file part')
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            image_path = "./static/uploads/"+file.filename
            image_paths.append(image_path)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Allowed image types are: jpg, png')
            return redirect(request.url)
    # Before this line we have images upload part and after this line we get predictions for each photo
    model = keras.models.load_model('../model/NeironAI.h5')
    classification = {}
    for path in image_paths:
        result = model_prediction(path, model)
        if isinstance(result, int):
            classification[path] = 'Undefined'
        else:
            max_prob_indx = np.argmax(result)
            max_prob_label = label_to_ids[max_prob_indx]
            max_prob = np.max(result)
            classification[path] = '%s (%.2f%%)' % (max_prob_label, max_prob*100)

    # return jsonify(classification) #this line is just for json type endpoint if it is needed
    return render_template('index.html', filenames = file_names, prediction = classification)

# This method is for displaying all images
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename = 'uploads/'+filename), code = 301)

if __name__ == '__main__':
    webbrowser.open("http://localhost:3000/")
    app.run(port = 3000, debug = True, use_reloader=False)