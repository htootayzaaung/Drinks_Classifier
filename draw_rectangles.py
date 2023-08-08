import os
import cv2

LOG_FILE = "image_log.txt"

def write_log(message):
    with open(LOG_FILE, 'a') as log:
        log.write(message + "\n")

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global drawing, top_left_pt, bottom_right_pt, display_img, clone

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        top_left_pt = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bottom_right_pt = (x, y)
        cv2.rectangle(display_img, top_left_pt, bottom_right_pt, (0, 0, 255), 5)  # Increased line thickness to 5
        cv2.imshow('Draw Rectangle', display_img)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = clone.copy()
            cv2.rectangle(img_copy, top_left_pt, (x, y), (0, 0, 255), 5)  # Increased line thickness to 5
            cv2.imshow('Draw Rectangle', img_copy)

if __name__ == '__main__':
    global drawing, top_left_pt, bottom_right_pt, display_img, clone

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as log:
            pass

    print("Keys: [d] - Delete, [s] - Save, [i] - Ignore, [q] - Quit")

    input_folder = "Images"

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                input_path = os.path.join(root, filename)

                # Check if image is already processed
                with open(LOG_FILE, 'r') as log:
                    if input_path in log.read():
                        continue

                # Load the image
                img = cv2.imread(input_path)
                clone = img.copy()
                drawing = False
                top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

                display_img = clone.copy()

                cv2.namedWindow('Draw Rectangle')
                cv2.setMouseCallback('Draw Rectangle', draw_rectangle)

                while True:
                    cv2.imshow('Draw Rectangle', display_img)
                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("d"):
                        os.remove(input_path)
                        write_log(f"Deleted: {input_path}")
                        print(f"Deleted: {input_path}")
                        break

                    elif key == ord("s"):
                        if top_left_pt != (-1, -1) and bottom_right_pt != (-1, -1):
                            roi = clone[top_left_pt[1]:bottom_right_pt[1], top_left_pt[0]:bottom_right_pt[0]]
                            cv2.imwrite(input_path, roi)
                            write_log(f"Cropped and saved: {input_path}")
                            print(f"Cropped and saved: {input_path}")
                        break

                    elif key == ord("i"):
                        write_log(f"Ignored: {input_path}")
                        print(f"Ignored: {input_path}")
                        break

                    elif key == ord("q"):
                        cv2.destroyAllWindows()
                        exit(0)

                cv2.destroyWindow('Draw Rectangle')
