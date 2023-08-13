import numpy as np
import os
import cv2
import glob
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from collections import Counter
from sklearn.metrics import classification_report
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Load the Data
X = []
Y = []

paths = [
    ('Images/coca_cola_images', 0),
    ('Images/pepsi_images', 1),
    ('Images/heineken_beer_images', 2)
]

for path, label in paths:
    for filename in glob.glob(os.path.join(path, "*.jpg")):
        img = cv2.imread(filename, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        X.append(img)
        Y.append(label)

shapes = [img.shape for img in X]
most_common_shape = Counter(shapes).most_common(1)[0][0]
X_resized = [cv2.resize(img, (most_common_shape[1], most_common_shape[0])) for img in X]

X = np.array(X_resized) / 255.0
Y = to_categorical(Y)

X_train, X_temp, y_train, y_temp = train_test_split(X, Y, test_size=0.3)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=X_train.shape[1:]))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
model_checkpoint = ModelCheckpoint("best_model.h5", save_best_only=True, monitor='val_loss')

history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val), callbacks=[early_stopping, model_checkpoint])

with open('training_logs.txt', 'w') as log_file:
    for epoch, (loss, acc, val_loss, val_acc) in enumerate(zip(history.history['loss'], history.history['accuracy'], history.history['val_loss'], history.history['val_accuracy'])):
        log_file.write(f"Epoch {epoch+1} - loss: {loss:.4f}, accuracy: {acc:.4f}, val_loss: {val_loss:.4f}, val_accuracy: {val_acc:.4f}\n")

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy*100:.2f}%")

y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)

report = classification_report(y_true_classes, y_pred_classes, target_names=["Coca-Cola", "Pepsi", "Heineken"])
with open('classification_report.txt', 'w') as report_file:
    report_file.write(report)
