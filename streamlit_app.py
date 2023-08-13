import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import cv2

# Load your pre-trained model
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

st.set_page_config(page_title="Quench Quest", page_icon="🍹")

st.title("Quench Quest")
st.write("## Drinks Classifier")
st.write("More drinks to be classified soon...")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    st.write("")
    st.write("Classifying...")

    label, confidence = predict_image(image)
    st.write(f"Predicted Brand: {label} with confidence: {confidence:.2f}")
else:
    st.write("Or capture an image from your webcam:")

    start_capture = st.button("Start Webcam")
    
    if start_capture:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            st.image(frame, channels="BGR", use_column_width=True)
            image = Image.fromarray(frame)
            label, confidence = predict_image(image)
            st.write(f"Predicted Brand: {label} with confidence: {confidence:.2f}")
