import cv2
import numpy as np
import tensorflow as tf
import glob
from tensorflow.keras.models import load_model

def load_most_common_shape():
    with open('shape.txt', 'r') as f:
        width, height = map(int, f.read().split())
    return (height, width)

# Load the trained model
model = load_model('trained_model.h5')

most_common_shape = load_most_common_shape()

# Define class labels
labels = ["Cola", "Pepsi", "Heineken"]

# Loop through each class's test folder, preprocess and predict
for label in labels:
    for image_path in glob.glob(f'test/{label.lower()}/*.jpg'):
        # Load image
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize to the shape used during training
        img_resized = cv2.resize(img, (most_common_shape[1], most_common_shape[0]))

        # Normalize
        img_normalized = np.array(img_resized) / 255.0

        # Reshape for model input
        img_input = np.expand_dims(img_normalized, axis=0)

        # Make prediction
        prediction = model.predict(img_input)
        predicted_class = labels[np.argmax(prediction)]

        print(f"Image: {image_path}, Predicted: {predicted_class}")
