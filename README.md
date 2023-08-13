# Drinks Classifier

**Contributors**: Htoo Tayza Aung, Min Bhone Thit

## Getting Started and Running the Program

1. **Setup**: 
    - Uncompress the zip files in the `Images` directory.

2. **Training the Model**:
    - Run the `evaluate_model.py` script:
        ```bash
        python3 evaluate_model.py
        ```
    - This process can take approximately 20 minutes or more.
    - Upon completion, this will generate a model named `trained_model.h5`.
    - This process will generate or overwrite `training_logs.txt` and `classification_report.txt` with scores of 99-100% for precision, recall, f1-score, and accuracy.

3. **Testing the Model**:
    - Run the `model_test.py` script for basic tests:
        ```bash
        python3 model_test.py
        ```
    - Observe that it passes 9 tests. (This step is optional).

4. **Launching the UI**:
    - Run `app.py` to open a user interface. This allows you to either:
        - Start a webcam to display the label and confidence in real-time.
        - Upload an image to see the label and confidence score.
        ```bash
        python3 app.py
        ```

## Notes:

Additional python scripts used during the development stage:

- `convert_2_jpg.py`: Converts all the images in the `Images` directory into `.jpg` format.

- `data_augmentation.py`: Produces copies of the original image with 5-degree rotation, -5-degree rotation, and mirrored image. These images are then populated into their respective directories.

- `draw_rectangles.py`: A smart image cropping tool. It lets you manually extract regions of interest from images. Run this program and follow on-screen instructions for its shortcuts. This tool was used for data pre-processing. If you terminate the program and restart it, it will remember where you left off. To start preprocessing from the beginning, empty the contents of `image_log.txt`.

