import os
import cv2
import json

def draw_rectangles(image_path, save_path):
    image = cv2.imread(image_path)
    clone = image.copy()
    rectangles = []

    def mouse_callback(event, x, y, flags, param):
        nonlocal rectangles
        if event == cv2.EVENT_LBUTTONDOWN:
            rectangles.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            rectangles[-1] = (rectangles[-1][0], y)

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)

    while True:
        cv2.imshow('Image', clone)
        key = cv2.waitKey(1)

        if key == ord('r'):
            # Remove the last drawn rectangle if 'r' is pressed
            if rectangles:
                rectangles.pop()

        elif key == ord('c'):
            # Clear all rectangles if 'c' is pressed
            rectangles = []

        elif key == ord('s'):
            # Save the rectangles to a JSON file if 's' is pressed
            with open(save_path, 'w') as f:
                json.dump(rectangles, f)
            print(f"Saved annotations to {save_path}")
            break

        elif key == 27:  # Press 'Esc' to exit without saving
            break

        clone = image.copy()
        for rect in rectangles:
            cv2.rectangle(clone, (rect[0], rect[1]), (image.shape[1], rect[1]), (0, 0, 255), -1)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    brands = [
        "Heineken beer",
        "Carlsberg beer",
        "Tiger beer",
        "Red Bull energy drink",
        "Coca Cola",
        "Pepsi"
    ]  # Add more brands as needed

    for brand in brands:
        brand_folder = f"Images/{brand.lower().replace(' ', '_')}_images"
        save_folder = f"Annotations/{brand.lower().replace(' ', '_')}_annotations"
        os.makedirs(save_folder, exist_ok=True)

        for filename in os.listdir(brand_folder):
            if filename.endswith(".jpg"):
                image_path = os.path.join(brand_folder, filename)
                save_path = os.path.join(save_folder, f"{filename.split('.')[0]}.json")

                if not os.path.exists(save_path):
                    draw_rectangles(image_path, save_path)
