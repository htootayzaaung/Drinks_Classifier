import os
import cv2

LOG_FILE = "image_log.txt"

def write_log(message):
    with open(LOG_FILE, 'a') as log:
        log.write(message + "\n")

def resize_image_to_fit_screen(image, screen_width, screen_height):
    h, w = image.shape[:2]
    aspect_ratio = w / h
    if w > screen_width:
        w = screen_width
        h = int(w / aspect_ratio)
    if h > screen_height:
        h = screen_height
        w = int(h * aspect_ratio)
    return cv2.resize(image, (w, h))

def draw_rectangle(event, x, y, flags, param):
    global drawing, top_left_pt, bottom_right_pt, img, clone, rect_drawn

    if event == cv2.EVENT_LBUTTONDOWN:
        if rect_drawn:
            img = clone.copy()
            cv2.imshow('Draw Rectangle', img)
            rect_drawn = False
        drawing = True
        top_left_pt = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bottom_right_pt = (x, y)
        cv2.rectangle(img, top_left_pt, bottom_right_pt, (0, 0, 255), 4)
        cv2.imshow('Draw Rectangle', img)
        rect_drawn = True

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        tmp_img = clone.copy()
        cv2.rectangle(tmp_img, top_left_pt, (x, y), (0, 0, 255), 4)
        cv2.imshow('Draw Rectangle', tmp_img)

if __name__ == '__main__':
    input_folder = "Images"

    # Globals
    drawing = False
    top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)
    rect_drawn = False

    screen_width = 1920  # modify these values to your screen dimensions
    screen_height = 1080

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as log:
            pass

    print("Keys: [d] - Delete, [s] - Save, [i] - Ignore, [q] - Quit")

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                input_path = os.path.join(root, filename)

                # Check if image is already processed
                with open(LOG_FILE, 'r') as log:
                    if input_path in log.read():
                        continue

                img = cv2.imread(input_path)
                img = resize_image_to_fit_screen(img, screen_width, screen_height)
                clone = img.copy()

                cv2.namedWindow('Draw Rectangle')
                cv2.setMouseCallback('Draw Rectangle', draw_rectangle)

                while True:
                    cv2.imshow('Draw Rectangle', img)
                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("d"):
                        os.remove(input_path)
                        write_log(f"Deleted: {input_path}")
                        print(f"Deleted: {input_path}")
                        break

                    elif key == ord("s"):
                        if top_left_pt != (-1, -1) and bottom_right_pt != (-1, -1):
                            cropped_img = clone[top_left_pt[1]:bottom_right_pt[1], top_left_pt[0]:bottom_right_pt[0]]
                            cv2.imwrite(input_path, cropped_img)
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
