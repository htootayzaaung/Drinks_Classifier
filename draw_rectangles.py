import os
import cv2

def manual_crop(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(('.jpg', '.png', '.jpeg')):  # Add other image formats if needed
                input_path = os.path.join(root, filename)
                output_path = os.path.join(output_folder, os.path.relpath(input_path, input_folder))

                # Load the image
                image = cv2.imread(input_path)

                # Calculate a resizing factor to fit within screen dimensions
                screen_height, screen_width = 1080, 1920  # Adjust these values according to your screen resolution
                max_display_size = (screen_width, screen_height)
                h, w = image.shape[:2]
                resize_factor = min(1.0, max_display_size[0] / w, max_display_size[1] / h)

                # Resize the image while maintaining aspect ratio
                resized_image = cv2.resize(image, None, fx=resize_factor, fy=resize_factor)

                # Display the image and let the user select the cropping region
                clone = resized_image.copy()
                roi = cv2.selectROI("Select ROI (Press Enter to Confirm, ESC to Exit)", clone, showCrosshair=True, fromCenter=False)

                # Handle the case where the user presses the ESC key
                if roi == (0, 0, 0, 0):
                    cv2.destroyAllWindows()
                    return

                cv2.destroyWindow("Select ROI")

                # Resize the cropping coordinates back to the original image size
                x, y, w, h = [int(coord / resize_factor) for coord in roi]

                # Crop the image based on the selected region
                cropped_image = image[y:y+h, x:x+w]

                # Overwrite the original image with the cropped version
                cv2.imwrite(input_path, cropped_image)

                # Display the image name in the terminal
                print(f"Cropped and saved: {input_path}")

if __name__ == "__main__":
    input_folder = "Images"  # Replace with the path to your input image folder
    output_folder = "Cropped_Images"  # Replace with the desired output folder

    manual_crop(input_folder, output_folder)
