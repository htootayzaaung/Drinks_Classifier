from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)

model = tf.keras.models.load_model('trained_model.h5')
labels = ["Coca Cola", "Pepsi", "Heineken"]

def predict_image(img):
    img_array = np.asarray(img) / 255.0
    img_array = tf.image.resize(img_array, (270, 230))
    img_array = tf.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    label = labels[np.argmax(predictions)]
    confidence = np.max(predictions)
    
    return label, confidence

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'file' in request.files:
        image = Image.open(request.files['file'].stream)
        label, confidence = predict_image(image)
        # This can be optimized further but keeping it simple for now
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode()
        return render_template('index.html', uploaded_image=f"data:image/jpeg;base64,{encoded_image}", label=label, confidence=confidence)
    return render_template('index.html')

@app.route('/predict-webcam', methods=['POST'])
def predict_webcam():
    image_data = request.json['image']
    decoded_image_data = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(decoded_image_data))
    label, confidence = predict_image(image)
    return jsonify({"label": label, "confidence": float(confidence)})

if __name__ == '__main__':
    app.run(debug=True)
